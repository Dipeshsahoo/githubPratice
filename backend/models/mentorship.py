"""
Mentorship model
"""

from datetime import datetime
from mongoengine import Document, fields

class MentorshipPost(Document):
    """Mentorship post model"""
    meta = {
        'collection': 'mentorship_posts',
        'indexes': ['user_id', 'is_approved']
    }
    
    user_id = fields.StringField(required=True)
    title = fields.StringField(max_length=255, required=True)
    description = fields.StringField(required=True)
    expertise_area = fields.StringField(max_length=255)
    availability_status = fields.StringField(max_length=20, default='available')
    is_approved = fields.BooleanField(default=False)
    created_at = fields.DateTimeField(default=datetime.utcnow)
    updated_at = fields.DateTimeField(default=datetime.utcnow)
    
    def save(self, *args, **kwargs):
        """Override save to update updated_at"""
        self.updated_at = datetime.utcnow()
        return super().save(*args, **kwargs)
    
    def to_dict(self, include_user=False):
        """Convert to dictionary"""
        data = {
            'id': str(self.id),
            'user_id': self.user_id,
            'title': self.title,
            'description': self.description,
            'expertise_area': self.expertise_area,
            'availability_status': self.availability_status,
            'is_approved': self.is_approved,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
        if include_user and self.user_id:
            from models.user import User
            user = User.objects(id=self.user_id).first()
            if user:
                data['user'] = user.to_dict(include_profile=True)
        return data
