"""
Mentorship routes
"""

from flask import Blueprint, request, jsonify
from extensions import db
from models.mentorship import MentorshipPost
from middleware.auth import alumni_required, admin_required
from flask_jwt_extended import get_jwt_identity

mentorship_bp = Blueprint('mentorship', __name__)

@mentorship_bp.route('', methods=['GET'])
def list_mentorship():
    """List mentorship posts"""
    expertise = request.args.get('expertise')
    availability = request.args.get('availability')
    approved_only = request.args.get('approved_only', 'true').lower() == 'true'
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    
    query = MentorshipPost.query
    
    if approved_only:
        query = query.filter(MentorshipPost.is_approved == True)
    
    if expertise:
        query = query.filter(MentorshipPost.expertise_area.ilike(f'%{expertise}%'))
    
    if availability:
        query = query.filter(MentorshipPost.availability_status == availability)
    
    query = query.order_by(MentorshipPost.created_at.desc())
    
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    
    posts = [post.to_dict(include_user=True) for post in pagination.items]
    
    return jsonify({
        'posts': posts,
        'total': pagination.total,
        'page': page,
        'per_page': per_page,
        'pages': pagination.pages
    }), 200

@mentorship_bp.route('/<int:post_id>', methods=['GET'])
def get_mentorship(post_id):
    """Get mentorship post"""
    post = MentorshipPost.query.get_or_404(post_id)
    
    # Only show approved posts to non-admins
    current_user_id = None
    try:
        from flask_jwt_extended import verify_jwt_in_request
        verify_jwt_in_request(optional=True)
        current_user_id = get_jwt_identity()
        from models.user import User
        user = User.query.get(current_user_id) if current_user_id else None
        if not user or user.role != 'admin':
            if not post.is_approved:
                return jsonify({'error': 'Post not found'}), 404
    except:
        if not post.is_approved:
            return jsonify({'error': 'Post not found'}), 404
    
    return jsonify(post.to_dict(include_user=True)), 200

@mentorship_bp.route('', methods=['POST'])
@alumni_required
def create_mentorship():
    """Create mentorship post"""
    data = request.get_json()
    
    required_fields = ['title', 'description']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'{field} is required'}), 400
    
    post = MentorshipPost(
        user_id=get_jwt_identity(),
        title=data['title'],
        description=data['description'],
        expertise_area=data.get('expertise_area'),
        availability_status=data.get('availability_status', 'available'),
        is_approved=False  # Requires admin approval
    )
    
    db.session.add(post)
    db.session.commit()
    
    return jsonify({
        'message': 'Mentorship post created. Awaiting approval.',
        'post': post.to_dict()
    }), 201

@mentorship_bp.route('/<int:post_id>', methods=['PUT'])
@alumni_required
def update_mentorship(post_id):
    """Update mentorship post"""
    post = MentorshipPost.query.get_or_404(post_id)
    user_id = get_jwt_identity()
    
    # Users can only update their own posts
    if post.user_id != user_id:
        return jsonify({'error': 'Permission denied'}), 403
    
    data = request.get_json()
    
    if 'title' in data:
        post.title = data['title']
    if 'description' in data:
        post.description = data['description']
    if 'expertise_area' in data:
        post.expertise_area = data['expertise_area']
    if 'availability_status' in data:
        post.availability_status = data['availability_status']
    
    # Reset approval status if content changed
    post.is_approved = False
    
    db.session.commit()
    
    return jsonify({
        'message': 'Post updated. Awaiting approval.',
        'post': post.to_dict()
    }), 200

@mentorship_bp.route('/<int:post_id>', methods=['DELETE'])
@alumni_required
def delete_mentorship(post_id):
    """Delete mentorship post"""
    post = MentorshipPost.query.get_or_404(post_id)
    user_id = get_jwt_identity()
    
    # Users can only delete their own posts (or admin)
    from models.user import User
    user = User.query.get(user_id)
    if post.user_id != user_id and user.role != 'admin':
        return jsonify({'error': 'Permission denied'}), 403
    
    db.session.delete(post)
    db.session.commit()
    
    return jsonify({'message': 'Post deleted successfully'}), 200

@mentorship_bp.route('/<int:post_id>/approve', methods=['POST'])
@admin_required
def approve_mentorship(post_id):
    """Approve mentorship post (admin only)"""
    post = MentorshipPost.query.get_or_404(post_id)
    post.is_approved = True
    db.session.commit()
    
    return jsonify({
        'message': 'Post approved successfully',
        'post': post.to_dict()
    }), 200
