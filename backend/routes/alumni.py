"""
Alumni routes
"""

from flask import Blueprint, request, jsonify
from models.user import User, Profile
from middleware.auth import login_required, alumni_required
from flask_jwt_extended import get_jwt_identity
from mongoengine import Q

alumni_bp = Blueprint('alumni', __name__)

@alumni_bp.route('', methods=['GET'])
def list_alumni():
    """List alumni with filters"""
    # Get filters
    search = request.args.get('search', '').strip()
    batch_year = request.args.get('batch_year', type=int)
    profession = request.args.get('profession', '').strip()
    location = request.args.get('location', '').strip()
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    
    # Get approved and verified alumni user IDs
    approved_users = User.objects(role='alumni', is_approved=True, is_verified=True).only('id')
    approved_user_ids = [str(u.id) for u in approved_users]
    
    # Build query
    query = Profile.objects(user_id__in=approved_user_ids)
    
    if search:
        query = query.filter(
            Q(first_name__icontains=search) |
            Q(last_name__icontains=search) |
            Q(profession__icontains=search) |
            Q(company__icontains=search)
        )
    
    if batch_year:
        query = query.filter(batch_year=batch_year)
    
    if profession:
        query = query.filter(profession__icontains=profession)
    
    if location:
        query = query.filter(location__icontains=location)
    
    # Pagination
    total = query.count()
    skip = (page - 1) * per_page
    profiles = query.skip(skip).limit(per_page)
    pages = (total + per_page - 1) // per_page
    
    # Get current user for contact info visibility
    current_user_id = None
    try:
        from flask_jwt_extended import verify_jwt_in_request
        verify_jwt_in_request(optional=True)
        current_user_id = get_jwt_identity()
    except:
        pass
    
    current_user = User.objects(id=current_user_id).first() if current_user_id else None
    
    alumni = []
    for profile in profiles:
        include_contact = current_user is not None
        alumni.append(profile.to_dict(include_contact=include_contact, requesting_user=current_user))
    
    return jsonify({
        'alumni': alumni,
        'total': total,
        'page': page,
        'per_page': per_page,
        'pages': pages
    }), 200

@alumni_bp.route('/<user_id>', methods=['GET'])
def get_alumni(user_id):
    """Get alumni profile"""
    user = User.objects(id=user_id).first()
    
    if not user or user.role != 'alumni' or not user.is_approved:
        return jsonify({'error': 'Alumni not found'}), 404
    
    # Get current user for contact info visibility
    current_user_id = None
    try:
        from flask_jwt_extended import verify_jwt_in_request
        verify_jwt_in_request(optional=True)
        current_user_id = get_jwt_identity()
    except:
        pass
    
    current_user = User.objects(id=current_user_id).first() if current_user_id else None
    
    profile = Profile.objects(user_id=user_id).first()
    include_contact = current_user is not None
    
    return jsonify({
        'user': user.to_dict(include_profile=True),
        'profile': profile.to_dict(include_contact=include_contact, requesting_user=current_user) if profile else None
    }), 200

@alumni_bp.route('/<user_id>', methods=['PUT'])
@alumni_required
def update_alumni(user_id):
    """Update alumni profile"""
    current_user_id = get_jwt_identity()
    user = User.objects(id=user_id).first()
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    # Users can only update their own profile (unless admin)
    current_user = User.objects(id=current_user_id).first()
    if str(current_user.id) != user_id and current_user.role != 'admin':
        return jsonify({'error': 'Permission denied'}), 403
    
    data = request.get_json()
    
    profile = Profile.objects(user_id=user_id).first()
    if not profile:
        profile = Profile(user_id=user_id)
    
    # Update profile fields
    if 'first_name' in data:
        profile.first_name = data['first_name']
    if 'last_name' in data:
        profile.last_name = data['last_name']
    if 'batch_year' in data:
        profile.batch_year = data['batch_year']
    if 'profession' in data:
        profile.profession = data['profession']
    if 'company' in data:
        profile.company = data['company']
    if 'location' in data:
        profile.location = data['location']
    if 'bio' in data:
        profile.bio = data['bio']
    if 'linkedin_url' in data:
        profile.linkedin_url = data['linkedin_url']
    if 'website_url' in data:
        profile.website_url = data['website_url']
    if 'show_contact_info' in data:
        profile.show_contact_info = data['show_contact_info']
    
    # Check if profile is complete
    required_fields = ['first_name', 'last_name', 'batch_year', 'profession']
    profile.is_profile_complete = all([
        getattr(profile, field) for field in required_fields
    ])
    
    profile.save()
    
    return jsonify({
        'message': 'Profile updated successfully',
        'profile': profile.to_dict(include_contact=True, requesting_user=current_user)
    }), 200

@alumni_bp.route('/<user_id>/complete-profile', methods=['POST'])
@alumni_required
def complete_profile(user_id):
    """Complete profile after first login"""
    current_user_id = get_jwt_identity()
    user = User.objects(id=user_id).first()
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    if str(current_user_id) != user_id:
        return jsonify({'error': 'Permission denied'}), 403
    
    data = request.get_json()
    
    profile = Profile.objects(user_id=user_id).first()
    if not profile:
        profile = Profile(user_id=user_id)
    
    # Required fields
    required_fields = ['first_name', 'last_name', 'batch_year', 'profession']
    for field in required_fields:
        if field not in data or not data[field]:
            return jsonify({'error': f'{field} is required'}), 400
        setattr(profile, field, data[field])
    
    # Optional fields
    optional_fields = ['company', 'location', 'bio', 'linkedin_url', 'website_url']
    for field in optional_fields:
        if field in data:
            setattr(profile, field, data[field])
    
    profile.is_profile_complete = True
    profile.save()
    
    return jsonify({
        'message': 'Profile completed successfully',
        'profile': profile.to_dict(include_contact=True, requesting_user=user)
    }), 200
