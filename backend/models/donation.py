"""
Donation model
"""

from datetime import datetime
from mongoengine import Document, fields

class Donation(Document):
    """Donation model"""
    meta = {
        'collection': 'donations',
        'indexes': ['user_id', 'status']
    }
    
    user_id = fields.StringField()
    donor_name = fields.StringField(max_length=255, required=True)
    donor_email = fields.EmailField()
    donor_mobile = fields.StringField(max_length=20)
    amount = fields.DecimalField(required=True, precision=10, decimal_places=2)
    purpose = fields.StringField(max_length=255)
    status = fields.StringField(max_length=20, default='pending')
    payment_method = fields.StringField(max_length=50)
    transaction_id = fields.StringField(max_length=255)
    notes = fields.StringField()
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
            'donor_name': self.donor_name,
            'donor_email': self.donor_email,
            'donor_mobile': self.donor_mobile,
            'amount': float(self.amount) if self.amount else None,
            'purpose': self.purpose,
            'status': self.status,
            'payment_method': self.payment_method,
            'transaction_id': self.transaction_id,
            'notes': self.notes,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
        if include_user and self.user_id:
            from models.user import User
            user = User.objects(id=self.user_id).first()
            if user:
                data['user'] = user.to_dict()
        return data
