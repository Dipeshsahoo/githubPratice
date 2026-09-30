"""
Authentication routes
"""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity, jwt_required
from models.user import User, Profile
from utils.auth import generate_verification_token
from utils.validation import validate_email, validate_mobile
from datetime import datetime

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    """Alumni registration"""
    data = request.get_json()
    
    # Validation
    email = data.get('email', '').strip().lower()
    password = data.get('password', '')
    mobile = data.get('mobile', '').strip()
    
    if not email or not password:
        return jsonify({'error': 'Email and password are required'}), 400
    
    # Validate email
    is_valid, error = validate_email(email)
    if not is_valid:
        return jsonify({'error': f'Invalid email: {error}'}), 400
    
    # Validate mobile if provided
    if mobile:
        is_valid, error = validate_mobile(mobile)
        if not is_valid:
            return jsonify({'error': error}), 400
    
    # Check if user exists
    if User.objects(email=email).first():
        return jsonify({'error': 'Email already registered'}), 409
    
    if mobile and User.objects(mobile=mobile).first():
        return jsonify({'error': 'Mobile number already registered'}), 409
    
    # Create user
    user = User(
        email=email,
        mobile=mobile if mobile else None,
        role='alumni',
        is_verified=False,
        is_approved=False,
        verification_token=generate_verification_token()
    )
    user.set_password(password)
    user.save()
    
    # Create profile placeholder
    profile = Profile(
        user_id=str(user.id),
        first_name=data.get('first_name', ''),
        last_name=data.get('last_name', ''),
        is_profile_complete=False
    )
    profile.save()
    
    return jsonify({
        'message': 'Registration successful. Please verify your email/mobile.',
        'user_id': str(user.id),
        'verification_token': user.verification_token  # In production, send via email/SMS
    }), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    """User login"""
    data = request.get_json()
    email = data.get('email', '').strip().lower()
    password = data.get('password', '')
    
    if not email or not password:
        return jsonify({'error': 'Email and password are required'}), 400
    
    user = User.objects(email=email).first()
    
    if not user or not user.check_password(password):
        return jsonify({'error': 'Invalid credentials'}), 401
    
    # Update last login
    user.last_login = datetime.utcnow()
    user.save()
    
    # Generate tokens
    access_token = create_access_token(identity=str(user.id))
    refresh_token = create_refresh_token(identity=str(user.id))
    
    return jsonify({
        'access_token': access_token,
        'refresh_token': refresh_token,
        'user': user.to_dict(include_profile=True)
    }), 200

@auth_bp.route('/verify', methods=['POST'])
def verify():
    """Verify email/mobile"""
    data = request.get_json()
    token = data.get('token', '')
    user_id = data.get('user_id')
    
    if not token or not user_id:
        return jsonify({'error': 'Token and user_id are required'}), 400
    
    user = User.objects(id=user_id).first()
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    if user.verification_token == token:
        user.is_verified = True
        user.verification_token = None
        user.save()
        return jsonify({'message': 'Verification successful'}), 200
    
    return jsonify({'error': 'Invalid verification token'}), 400

@auth_bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    """Refresh access token"""
    user_id = get_jwt_identity()
    access_token = create_access_token(identity=user_id)
    return jsonify({'access_token': access_token}), 200

@auth_bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    """Logout (client should discard tokens)"""
    return jsonify({'message': 'Logged out successfully'}), 200

@auth_bp.route('/forgot-password', methods=['POST'])
def forgot_password():
    """Request password reset"""
    data = request.get_json()
    email = data.get('email', '').strip().lower()
    
    if not email:
        return jsonify({'error': 'Email is required'}), 400
    
    user = User.objects(email=email).first()
    if user:
        # Generate reset token
        user.reset_token = generate_verification_token()
        from datetime import timedelta
        user.reset_token_expires = datetime.utcnow() + timedelta(hours=1)
        user.save()
        # In production, send email with reset token
    
    # Always return success to prevent email enumeration
    return jsonify({'message': 'If email exists, reset link has been sent'}), 200

@auth_bp.route('/reset-password', methods=['POST'])
def reset_password():
    """Reset password with token"""
    data = request.get_json()
    token = data.get('token', '')
    new_password = data.get('password', '')
    
    if not token or not new_password:
        return jsonify({'error': 'Token and password are required'}), 400
    
    user = User.objects(reset_token=token).first()
    if not user or not user.reset_token_expires or user.reset_token_expires < datetime.utcnow():
        return jsonify({'error': 'Invalid or expired reset token'}), 400
    
    user.set_password(new_password)
    user.reset_token = None
    user.reset_token_expires = None
    user.save()
    
    return jsonify({'message': 'Password reset successful'}), 200
