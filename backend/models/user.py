"""
User and Profile models
"""

from datetime import datetime
from mongoengine import Document, EmbeddedDocument, fields
import bcrypt

class User(Document):
    """User model for authentication"""
    meta = {
        'collection': 'users',
        'indexes': ['email', 'mobile']
    }
    
    email = fields.EmailField(required=True, unique=True)
    mobile = fields.StringField(max_length=20, unique=True, sparse=True)
    password_hash = fields.StringField(required=True)
    role = fields.StringField(max_length=20, default='alumni', required=True)
    is_verified = fields.BooleanField(default=False)
    is_approved = fields.BooleanField(default=False)
    verification_token = fields.StringField(max_length=255)
    reset_token = fields.StringField(max_length=255)
    reset_token_expires = fields.DateTimeField()
    created_at = fields.DateTimeField(default=datetime.utcnow)
    updated_at = fields.DateTimeField(default=datetime.utcnow)
    last_login = fields.DateTimeField()
    
    def set_password(self, password):
        """Hash and set password"""
        self.password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        self.save()
    
    def check_password(self, password):
        """Verify password"""
        return bcrypt.checkpw(password.encode('utf-8'), self.password_hash.encode('utf-8'))
    
    def save(self, *args, **kwargs):
        """Override save to update updated_at"""
        self.updated_at = datetime.utcnow()
        return super().save(*args, **kwargs)
    
    def to_dict(self, include_profile=False):
        """Convert to dictionary"""
        profile = Profile.objects(user_id=str(self.id)).first()
        data = {
            'id': str(self.id),
            'email': self.email,
            'mobile': self.mobile,
            'role': self.role,
            'is_verified': self.is_verified,
            'is_approved': self.is_approved,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'last_login': self.last_login.isoformat() if self.last_login else None
        }
        if include_profile and profile:
            data['profile'] = profile.to_dict()
        return data

class Profile(Document):
    """Extended user profile"""
    meta = {
        'collection': 'profiles',
        'indexes': ['user_id', 'batch_year', 'profession', 'location']
    }
    
    user_id = fields.StringField(required=True, unique=True)
    first_name = fields.StringField(max_length=100, required=True)
    last_name = fields.StringField(max_length=100, required=True)
    batch_year = fields.IntField()
    profession = fields.StringField(max_length=255)
    company = fields.StringField(max_length=255)
    location = fields.StringField(max_length=255)
    bio = fields.StringField()
    profile_picture = fields.StringField(max_length=255)
    linkedin_url = fields.URLField()
    website_url = fields.URLField()
    is_profile_complete = fields.BooleanField(default=False)
    show_contact_info = fields.BooleanField(default=True)
    created_at = fields.DateTimeField(default=datetime.utcnow)
    updated_at = fields.DateTimeField(default=datetime.utcnow)
    
    def save(self, *args, **kwargs):
        """Override save to update updated_at"""
        self.updated_at = datetime.utcnow()
        return super().save(*args, **kwargs)
    
    def to_dict(self, include_contact=False, requesting_user=None):
        """Convert to dictionary"""
        data = {
            'id': str(self.id),
            'user_id': self.user_id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'batch_year': self.batch_year,
            'profession': self.profession,
            'company': self.company,
            'location': self.location,
            'bio': self.bio,
            'profile_picture': self.profile_picture,
            'linkedin_url': self.linkedin_url,
            'website_url': self.website_url,
            'is_profile_complete': self.is_profile_complete,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
        
        # Include contact info only if requested and allowed
        if include_contact and requesting_user and (str(requesting_user.id) == self.user_id or requesting_user.role == 'admin'):
            user = User.objects(id=self.user_id).first()
            if user:
                data['email'] = user.email
                data['mobile'] = user.mobile
        
        return data
    
    @property
    def full_name(self):
        """Get full name"""
        return f"{self.first_name} {self.last_name}"
