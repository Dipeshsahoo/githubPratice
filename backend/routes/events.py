"""
Events routes
"""

from flask import Blueprint, request, jsonify
from extensions import db
from models.event import Event, EventRegistration
from models.user import User
from middleware.auth import login_required, admin_required, alumni_required
from flask_jwt_extended import get_jwt_identity
from datetime import datetime
from utils.qr_code import generate_qr_code_image

events_bp = Blueprint('events', __name__)

@events_bp.route('', methods=['GET'])
def list_events():
    """List events"""
    event_type = request.args.get('type')
    is_jubilee = request.args.get('is_jubilee', type=bool)
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    
    query = Event.query
    
    if event_type:
        query = query.filter(Event.event_type == event_type)
    
    if is_jubilee is not None:
        query = query.filter(Event.is_jubilee_event == is_jubilee)
    
    query = query.order_by(Event.start_date.desc())
    
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    
    events = [event.to_dict() for event in pagination.items]
    
    return jsonify({
        'events': events,
        'total': pagination.total,
        'page': page,
        'per_page': per_page,
        'pages': pagination.pages
    }), 200

@events_bp.route('/<int:event_id>', methods=['GET'])
def get_event(event_id):
    """Get event details"""
    event = Event.query.get_or_404(event_id)
    
    # Check if user is registered
    current_user_id = None
    is_registered = False
    registration = None
    
    try:
        from flask_jwt_extended import verify_jwt_in_request
        verify_jwt_in_request(optional=True)
        current_user_id = get_jwt_identity()
        if current_user_id:
            registration = EventRegistration.query.filter_by(
                event_id=event_id,
                user_id=current_user_id
            ).first()
            is_registered = registration is not None
    except:
        pass
    
    event_dict = event.to_dict(include_registrations=True)
    event_dict['is_registered'] = is_registered
    if registration:
        event_dict['registration'] = registration.to_dict()
    
    return jsonify(event_dict), 200

@events_bp.route('', methods=['POST'])
@admin_required
def create_event():
    """Create event (admin only)"""
    data = request.get_json()
    
    required_fields = ['title', 'start_date']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'{field} is required'}), 400
    
    event = Event(
        title=data['title'],
        description=data.get('description'),
        event_type=data.get('event_type', 'other'),
        start_date=datetime.fromisoformat(data['start_date'].replace('Z', '+00:00')),
        end_date=datetime.fromisoformat(data['end_date'].replace('Z', '+00:00')) if data.get('end_date') else None,
        location=data.get('location'),
        venue=data.get('venue'),
        max_participants=data.get('max_participants'),
        registration_deadline=datetime.fromisoformat(data['registration_deadline'].replace('Z', '+00:00')) if data.get('registration_deadline') else None,
        is_jubilee_event=data.get('is_jubilee_event', False),
        created_by=get_jwt_identity()
    )
    
    db.session.add(event)
    db.session.commit()
    
    return jsonify({
        'message': 'Event created successfully',
        'event': event.to_dict()
    }), 201

@events_bp.route('/<int:event_id>', methods=['PUT'])
@admin_required
def update_event(event_id):
    """Update event (admin only)"""
    event = Event.query.get_or_404(event_id)
    data = request.get_json()
    
    if 'title' in data:
        event.title = data['title']
    if 'description' in data:
        event.description = data['description']
    if 'event_type' in data:
        event.event_type = data['event_type']
    if 'start_date' in data:
        event.start_date = datetime.fromisoformat(data['start_date'].replace('Z', '+00:00'))
    if 'end_date' in data:
        event.end_date = datetime.fromisoformat(data['end_date'].replace('Z', '+00:00')) if data['end_date'] else None
    if 'location' in data:
        event.location = data['location']
    if 'venue' in data:
        event.venue = data['venue']
    if 'max_participants' in data:
        event.max_participants = data['max_participants']
    if 'registration_deadline' in data:
        event.registration_deadline = datetime.fromisoformat(data['registration_deadline'].replace('Z', '+00:00')) if data['registration_deadline'] else None
    if 'is_jubilee_event' in data:
        event.is_jubilee_event = data['is_jubilee_event']
    
    db.session.commit()
    
    return jsonify({
        'message': 'Event updated successfully',
        'event': event.to_dict()
    }), 200

@events_bp.route('/<int:event_id>', methods=['DELETE'])
@admin_required
def delete_event(event_id):
    """Delete event (admin only)"""
    event = Event.query.get_or_404(event_id)
    db.session.delete(event)
    db.session.commit()
    
    return jsonify({'message': 'Event deleted successfully'}), 200

@events_bp.route('/<int:event_id>/register', methods=['POST'])
@alumni_required
def register_event(event_id):
    """Register for event"""
    event = Event.query.get_or_404(event_id)
    user_id = get_jwt_identity()
    
    # Check if already registered
    existing = EventRegistration.query.filter_by(
        event_id=event_id,
        user_id=user_id
    ).first()
    
    if existing:
        return jsonify({'error': 'Already registered for this event'}), 409
    
    # Check max participants
    if event.max_participants:
        current_count = EventRegistration.query.filter_by(event_id=event_id).count()
        if current_count >= event.max_participants:
            return jsonify({'error': 'Event is full'}), 400
    
    # Check registration deadline
    if event.registration_deadline and datetime.utcnow() > event.registration_deadline:
        return jsonify({'error': 'Registration deadline has passed'}), 400
    
    # Create registration
    registration = EventRegistration(
        event_id=event_id,
        user_id=user_id
    )
    registration.generate_qr_code()
    
    db.session.add(registration)
    db.session.commit()
    
    # Generate QR code image
    qr_image = generate_qr_code_image(registration.qr_code)
    
    return jsonify({
        'message': 'Registered successfully',
        'registration': registration.to_dict(),
        'qr_code_image': qr_image
    }), 201

@events_bp.route('/<int:event_id>/checkin', methods=['POST'])
@admin_required
def checkin_event(event_id):
    """QR code check-in (admin only)"""
    data = request.get_json()
    qr_code = data.get('qr_code')
    
    if not qr_code:
        return jsonify({'error': 'QR code is required'}), 400
    
    registration = EventRegistration.query.filter_by(
        event_id=event_id,
        qr_code=qr_code
    ).first()
    
    if not registration:
        return jsonify({'error': 'Invalid QR code'}), 404
    
    if registration.is_checked_in:
        return jsonify({'error': 'Already checked in'}), 409
    
    registration.is_checked_in = True
    registration.check_in_time = datetime.utcnow()
    db.session.commit()
    
    return jsonify({
        'message': 'Check-in successful',
        'registration': registration.to_dict(include_user=True)
    }), 200
