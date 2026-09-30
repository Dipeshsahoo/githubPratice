"""
Job models
"""

from datetime import datetime
from mongoengine import Document, fields

class JobPosting(Document):
    """Job posting model"""
    meta = {
        'collection': 'job_postings',
        'indexes': ['user_id', 'is_active', 'is_approved']
    }
    
    user_id = fields.StringField(required=True)
    title = fields.StringField(max_length=255, required=True)
    company = fields.StringField(max_length=255, required=True)
    description = fields.StringField(required=True)
    location = fields.StringField(max_length=255)
    job_type = fields.StringField(max_length=50)
    application_deadline = fields.DateTimeField()
    application_link = fields.StringField(max_length=255)
    is_approved = fields.BooleanField(default=False)
    is_active = fields.BooleanField(default=True)
    created_at = fields.DateTimeField(default=datetime.utcnow)
    updated_at = fields.DateTimeField(default=datetime.utcnow)
    
    def save(self, *args, **kwargs):
        """Override save to update updated_at"""
        self.updated_at = datetime.utcnow()
        return super().save(*args, **kwargs)
    
    def to_dict(self, include_user=False, include_applications=False):
        """Convert to dictionary"""
        application_count = None
        if include_applications:
            application_count = JobApplication.objects(job_posting_id=str(self.id)).count()
        
        data = {
            'id': str(self.id),
            'user_id': self.user_id,
            'title': self.title,
            'company': self.company,
            'description': self.description,
            'location': self.location,
            'job_type': self.job_type,
            'application_deadline': self.application_deadline.isoformat() if self.application_deadline else None,
            'application_link': self.application_link,
            'is_approved': self.is_approved,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'application_count': application_count
        }
        if include_user and self.user_id:
            from models.user import User
            user = User.objects(id=self.user_id).first()
            if user:
                data['user'] = user.to_dict(include_profile=True)
        return data

class JobApplication(Document):
    """Job application model"""
    meta = {
        'collection': 'job_applications',
        'indexes': ['job_posting_id', 'applicant_id'],
        'unique_with': ['job_posting_id', 'applicant_id']
    }
    
    job_posting_id = fields.StringField(required=True)
    applicant_id = fields.StringField(required=True)
    resume_path = fields.StringField(max_length=255)
    cover_letter = fields.StringField()
    status = fields.StringField(max_length=20, default='pending')
    applied_at = fields.DateTimeField(default=datetime.utcnow)
    
    def to_dict(self, include_applicant=False):
        """Convert to dictionary"""
        data = {
            'id': str(self.id),
            'job_posting_id': self.job_posting_id,
            'applicant_id': self.applicant_id,
            'resume_path': self.resume_path,
            'cover_letter': self.cover_letter,
            'status': self.status,
            'applied_at': self.applied_at.isoformat() if self.applied_at else None
        }
        if include_applicant and self.applicant_id:
            from models.user import User
            applicant = User.objects(id=self.applicant_id).first()
            if applicant:
                data['applicant'] = applicant.to_dict(include_profile=True)
        return data
