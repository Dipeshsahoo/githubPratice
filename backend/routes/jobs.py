"""
Jobs routes
"""

from flask import Blueprint, request, jsonify
from extensions import db
from models.job import JobPosting, JobApplication
from middleware.auth import alumni_required, admin_required
from flask_jwt_extended import get_jwt_identity
from utils.file_upload import allowed_file, save_uploaded_file
from datetime import datetime

jobs_bp = Blueprint('jobs', __name__)

@jobs_bp.route('', methods=['GET'])
def list_jobs():
    """List job postings"""
    job_type = request.args.get('job_type')
    location = request.args.get('location')
    active_only = request.args.get('active_only', 'true').lower() == 'true'
    approved_only = request.args.get('approved_only', 'true').lower() == 'true'
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    
    query = JobPosting.query
    
    if active_only:
        query = query.filter(JobPosting.is_active == True)
    
    if approved_only:
        query = query.filter(JobPosting.is_approved == True)
    
    if job_type:
        query = query.filter(JobPosting.job_type == job_type)
    
    if location:
        query = query.filter(JobPosting.location.ilike(f'%{location}%'))
    
    # Filter expired deadlines
    query = query.filter(
        (JobPosting.application_deadline.is_(None)) |
        (JobPosting.application_deadline > datetime.utcnow())
    )
    
    query = query.order_by(JobPosting.created_at.desc())
    
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    
    jobs = [job.to_dict(include_user=True) for job in pagination.items]
    
    return jsonify({
        'jobs': jobs,
        'total': pagination.total,
        'page': page,
        'per_page': per_page,
        'pages': pagination.pages
    }), 200

@jobs_bp.route('/<int:job_id>', methods=['GET'])
def get_job(job_id):
    """Get job posting"""
    job = JobPosting.query.get_or_404(job_id)
    
    # Only show approved jobs to non-admins
    current_user_id = None
    try:
        from flask_jwt_extended import verify_jwt_in_request
        verify_jwt_in_request(optional=True)
        current_user_id = get_jwt_identity()
        from models.user import User
        user = User.query.get(current_user_id) if current_user_id else None
        if not user or user.role != 'admin':
            if not job.is_approved or not job.is_active:
                return jsonify({'error': 'Job not found'}), 404
    except:
        if not job.is_approved or not job.is_active:
            return jsonify({'error': 'Job not found'}), 404
    
    return jsonify(job.to_dict(include_user=True)), 200

@jobs_bp.route('', methods=['POST'])
@alumni_required
def create_job():
    """Create job posting"""
    data = request.get_json()
    
    required_fields = ['title', 'company', 'description']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'{field} is required'}), 400
    
    job = JobPosting(
        user_id=get_jwt_identity(),
        title=data['title'],
        company=data['company'],
        description=data['description'],
        location=data.get('location'),
        job_type=data.get('job_type'),
        application_deadline=datetime.fromisoformat(data['application_deadline'].replace('Z', '+00:00')) if data.get('application_deadline') else None,
        application_link=data.get('application_link'),
        is_approved=False,  # Requires admin approval
        is_active=True
    )
    
    db.session.add(job)
    db.session.commit()
    
    return jsonify({
        'message': 'Job posting created. Awaiting approval.',
        'job': job.to_dict()
    }), 201

@jobs_bp.route('/<int:job_id>', methods=['PUT'])
@alumni_required
def update_job(job_id):
    """Update job posting"""
    job = JobPosting.query.get_or_404(job_id)
    user_id = get_jwt_identity()
    
    # Users can only update their own posts
    if job.user_id != user_id:
        return jsonify({'error': 'Permission denied'}), 403
    
    data = request.get_json()
    
    if 'title' in data:
        job.title = data['title']
    if 'company' in data:
        job.company = data['company']
    if 'description' in data:
        job.description = data['description']
    if 'location' in data:
        job.location = data['location']
    if 'job_type' in data:
        job.job_type = data['job_type']
    if 'application_deadline' in data:
        job.application_deadline = datetime.fromisoformat(data['application_deadline'].replace('Z', '+00:00')) if data['application_deadline'] else None
    if 'application_link' in data:
        job.application_link = data['application_link']
    if 'is_active' in data:
        job.is_active = data['is_active']
    
    # Reset approval status if content changed
    job.is_approved = False
    
    db.session.commit()
    
    return jsonify({
        'message': 'Job updated. Awaiting approval.',
        'job': job.to_dict()
    }), 200

@jobs_bp.route('/<int:job_id>', methods=['DELETE'])
@alumni_required
def delete_job(job_id):
    """Delete job posting"""
    job = JobPosting.query.get_or_404(job_id)
    user_id = get_jwt_identity()
    
    # Users can only delete their own posts (or admin)
    from models.user import User
    user = User.query.get(user_id)
    if job.user_id != user_id and user.role != 'admin':
        return jsonify({'error': 'Permission denied'}), 403
    
    db.session.delete(job)
    db.session.commit()
    
    return jsonify({'message': 'Job deleted successfully'}), 200

@jobs_bp.route('/<int:job_id>/apply', methods=['POST'])
@alumni_required
def apply_job(job_id):
    """Apply for job"""
    job = JobPosting.query.get_or_404(job_id)
    
    if not job.is_approved or not job.is_active:
        return jsonify({'error': 'Job is not available'}), 400
    
    if job.application_deadline and datetime.utcnow() > job.application_deadline:
        return jsonify({'error': 'Application deadline has passed'}), 400
    
    user_id = get_jwt_identity()
    
    # Check if already applied
    existing = JobApplication.query.filter_by(
        job_posting_id=job_id,
        applicant_id=user_id
    ).first()
    
    if existing:
        return jsonify({'error': 'Already applied for this job'}), 409
    
    data = request.get_json()
    
    # Handle resume upload if provided
    resume_path = None
    if 'resume' in request.files:
        file = request.files['resume']
        if file and allowed_file(file.filename):
            result = save_uploaded_file(file, 'resumes')
            if result:
                resume_path = result['file_path']
    
    application = JobApplication(
        job_posting_id=job_id,
        applicant_id=user_id,
        resume_path=resume_path,
        cover_letter=data.get('cover_letter'),
        status='pending'
    )
    
    db.session.add(application)
    db.session.commit()
    
    return jsonify({
        'message': 'Application submitted successfully',
        'application': application.to_dict()
    }), 201

@jobs_bp.route('/<int:job_id>/approve', methods=['POST'])
@admin_required
def approve_job(job_id):
    """Approve job posting (admin only)"""
    job = JobPosting.query.get_or_404(job_id)
    job.is_approved = True
    db.session.commit()
    
    return jsonify({
        'message': 'Job approved successfully',
        'job': job.to_dict()
    }), 200
