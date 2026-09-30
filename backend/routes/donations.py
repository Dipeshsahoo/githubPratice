"""
Donations routes
"""

from flask import Blueprint, request, jsonify
from extensions import db
from models.donation import Donation
from middleware.auth import admin_required
from flask_jwt_extended import get_jwt_identity
from decimal import Decimal

donations_bp = Blueprint('donations', __name__)

@donations_bp.route('', methods=['GET'])
@admin_required
def list_donations():
    """List donations (admin only)"""
    status = request.args.get('status')
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    
    query = Donation.query
    
    if status:
        query = query.filter(Donation.status == status)
    
    query = query.order_by(Donation.created_at.desc())
    
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    
    donations = [donation.to_dict() for donation in pagination.items]
    
    # Calculate totals
    total_amount = db.session.query(db.func.sum(Donation.amount)).filter(
        Donation.status == 'completed'
    ).scalar() or Decimal('0')
    
    return jsonify({
        'donations': donations,
        'total': pagination.total,
        'page': page,
        'per_page': per_page,
        'pages': pagination.pages,
        'total_amount': float(total_amount)
    }), 200

@donations_bp.route('', methods=['POST'])
def create_donation():
    """Create donation (public)"""
    data = request.get_json()
    
    required_fields = ['donor_name', 'amount']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'{field} is required'}), 400
    
    try:
        amount = Decimal(str(data['amount']))
        if amount <= 0:
            return jsonify({'error': 'Amount must be greater than 0'}), 400
    except:
        return jsonify({'error': 'Invalid amount'}), 400
    
    # Get user_id if logged in
    user_id = None
    try:
        from flask_jwt_extended import verify_jwt_in_request
        verify_jwt_in_request(optional=True)
        user_id = get_jwt_identity()
    except:
        pass
    
    donation = Donation(
        user_id=user_id,
        donor_name=data['donor_name'],
        donor_email=data.get('donor_email'),
        donor_mobile=data.get('donor_mobile'),
        amount=amount,
        purpose=data.get('purpose'),
        status='pending',
        payment_method=data.get('payment_method'),
        notes=data.get('notes')
    )
    
    db.session.add(donation)
    db.session.commit()
    
    return jsonify({
        'message': 'Donation recorded. Admin will process it.',
        'donation': donation.to_dict()
    }), 201

@donations_bp.route('/<int:donation_id>', methods=['PUT'])
@admin_required
def update_donation(donation_id):
    """Update donation status (admin only)"""
    donation = Donation.query.get_or_404(donation_id)
    data = request.get_json()
    
    if 'status' in data:
        if data['status'] not in ['pending', 'approved', 'rejected', 'completed']:
            return jsonify({'error': 'Invalid status'}), 400
        donation.status = data['status']
    
    if 'payment_method' in data:
        donation.payment_method = data['payment_method']
    
    if 'transaction_id' in data:
        donation.transaction_id = data['transaction_id']
    
    if 'notes' in data:
        donation.notes = data['notes']
    
    db.session.commit()
    
    return jsonify({
        'message': 'Donation updated successfully',
        'donation': donation.to_dict()
    }), 200
