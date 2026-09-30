"""
Event models
"""

from datetime import datetime
from mongoengine import Document, fields
import uuid

class Event(Document):
    """Event model"""
    meta = {
        'collection': 'events',
        'indexes': ['start_date', 'is_jubilee_event', 'created_by']
    }
    
    title = fields.StringField(max_length=255, required=True)
    description = fields.StringField()
    event_type = fields.StringField(max_length=50)
    start_date = fields.DateTimeField(required=True)
    end_date = fields.DateTimeField()
    location = fields.StringField(max_length=255)
    venue = fields.StringField(max_length=255)
    max_participants = fields.IntField()
    registration_deadline = fields.DateTimeField()
    is_jubilee_event = fields.BooleanField(default=False)
    created_by = fields.StringField()
    created_at = fields.DateTimeField(default=datetime.utcnow)
    updated_at = fields.DateTimeField(default=datetime.utcnow)
    
    def save(self, *args, **kwargs):
        """Override save to update updated_at"""
        self.updated_at = datetime.utcnow()
        return super().save(*args, **kwargs)
    
    def to_dict(self, include_registrations=False):
        """Convert to dictionary"""
        registration_count = None
        if include_registrations:
            registration_count = EventRegistration.objects(event_id=str(self.id)).count()
        
        data = {
            'id': str(self.id),
            'title': self.title,
            'description': self.description,
            'event_type': self.event_type,
            'start_date': self.start_date.isoformat() if self.start_date else None,
            'end_date': self.end_date.isoformat() if self.end_date else None,
            'location': self.location,
            'venue': self.venue,
            'max_participants': self.max_participants,
            'registration_deadline': self.registration_deadline.isoformat() if self.registration_deadline else None,
            'is_jubilee_event': self.is_jubilee_event,
            'created_by': self.created_by,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'registration_count': registration_count
        }
        return data

class EventRegistration(Document):
    """Event registration model"""
    meta = {
        'collection': 'event_registrations',
        'indexes': ['event_id', 'user_id', 'qr_code'],
        'unique_with': ['event_id', 'user_id']
    }
    
    event_id = fields.StringField(required=True)
    user_id = fields.StringField(required=True)
    qr_code = fields.StringField(max_length=255, unique=True)
    check_in_time = fields.DateTimeField()
    is_checked_in = fields.BooleanField(default=False)
    registration_date = fields.DateTimeField(default=datetime.utcnow)
    
    def generate_qr_code(self):
        """Generate unique QR code"""
        if not self.qr_code:
            self.qr_code = f"{self.event_id}_{self.user_id}_{uuid.uuid4().hex[:8]}"
        return self.qr_code
    
    def to_dict(self, include_user=False):
        """Convert to dictionary"""
        data = {
            'id': str(self.id),
            'event_id': self.event_id,
            'user_id': self.user_id,
            'qr_code': self.qr_code,
            'check_in_time': self.check_in_time.isoformat() if self.check_in_time else None,
            'is_checked_in': self.is_checked_in,
            'registration_date': self.registration_date.isoformat() if self.registration_date else None
        }
        if include_user:
            from models.user import User
            user = User.objects(id=self.user_id).first()
            if user:
                data['user'] = user.to_dict(include_profile=True)
        return data
