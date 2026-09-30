"""
Admin routes
"""

from flask import Blueprint, request, jsonify
from extensions import db
from models.user import User, Profile
from models.event import Event, EventRegistration
from models.news import News
from models.mentorship import MentorshipPost
from models.job import JobPosting
from models.donation import Donation
from middleware.auth import admin_required
from sqlalchemy import func

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/stats', methods=['GET'])
@admin_required
def get_stats():
    """Get dashboard statistics"""
    stats = {
        'users': {
            'total': User.query.count(),
            'alumni': User.query.filter_by(role='alumni').count(),
            'approved': User.query.filter_by(is_approved=True).count(),
            'pending_approval': User.query.filter_by(is_approved=False, role='alumni').count()
        },
        'events': {
            'total': Event.query.count(),
            'upcoming': Event.query.filter(Event.start_date > func.now()).count(),
            'jubilee_events': Event.query.filter_by(is_jubilee_event=True).count()
        },
        'news': {
            'total': News.query.count(),
            'published': News.query.filter_by(is_published=True).count()
        },
        'mentorship': {
            'total': MentorshipPost.query.count(),
            'approved': MentorshipPost.query.filter_by(is_approved=True).count(),
            'pending': MentorshipPost.query.filter_by(is_approved=False).count()
        },
        'jobs': {
            'total': JobPosting.query.count(),
            'active': JobPosting.query.filter_by(is_active=True, is_approved=True).count(),
            'pending': JobPosting.query.filter_by(is_approved=False).count()
        },
        'donations': {
            'total': Donation.query.count(),
            'pending': Donation.query.filter_by(status='pending').count(),
            'completed': Donation.query.filter_by(status='completed').count(),
            'total_amount': float(db.session.query(func.sum(Donation.amount)).filter(
                Donation.status == 'completed'
            ).scalar() or 0)
        }
    }
    
    return jsonify(stats), 200

@admin_bp.route('/users', methods=['GET'])
@admin_required
def list_users():
    """List all users"""
    role = request.args.get('role')
    is_approved = request.args.get('is_approved')
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    
    query = User.query
    
    if role:
        query = query.filter(User.role == role)
    
    if is_approved is not None:
        query = query.filter(User.is_approved == (is_approved.lower() == 'true'))
    
    query = query.order_by(User.created_at.desc())
    
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    
    users = [user.to_dict(include_profile=True) for user in pagination.items]
    
    return jsonify({
        'users': users,
        'total': pagination.total,
        'page': page,
        'per_page': per_page,
        'pages': pagination.pages
    }), 200

@admin_bp.route('/users/<int:user_id>/approve', methods=['PUT'])
@admin_required
def approve_user(user_id):
    """Approve user account"""
    user = User.query.get_or_404(user_id)
    user.is_approved = True
    db.session.commit()
    
    return jsonify({
        'message': 'User approved successfully',
        'user': user.to_dict(include_profile=True)
    }), 200

@admin_bp.route('/users/<int:user_id>/role', methods=['PUT'])
@admin_required
def change_user_role(user_id):
    """Change user role"""
    user = User.query.get_or_404(user_id)
    data = request.get_json()
    
    new_role = data.get('role')
    if new_role not in ['admin', 'alumni', 'visitor']:
        return jsonify({'error': 'Invalid role'}), 400
    
    user.role = new_role
    db.session.commit()
    
    return jsonify({
        'message': 'User role updated successfully',
        'user': user.to_dict(include_profile=True)
    }), 200
