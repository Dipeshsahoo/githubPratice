"""
News model
"""

from datetime import datetime
from mongoengine import Document, fields

class News(Document):
    """News and announcements model"""
    meta = {
        'collection': 'news',
        'indexes': ['is_published', 'published_at', 'created_at', 'author_id']
    }
    
    title = fields.StringField(max_length=255, required=True)
    content = fields.StringField(required=True)
    category = fields.StringField(max_length=50)
    author_id = fields.StringField()
    is_published = fields.BooleanField(default=False)
    published_at = fields.DateTimeField()
    created_at = fields.DateTimeField(default=datetime.utcnow)
    updated_at = fields.DateTimeField(default=datetime.utcnow)
    
    def save(self, *args, **kwargs):
        """Override save to update updated_at"""
        self.updated_at = datetime.utcnow()
        return super().save(*args, **kwargs)
    
    def to_dict(self, include_author=False):
        """Convert to dictionary"""
        data = {
            'id': str(self.id),
            'title': self.title,
            'content': self.content,
            'category': self.category,
            'author_id': self.author_id,
            'is_published': self.is_published,
            'published_at': self.published_at.isoformat() if self.published_at else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
        if include_author and self.author_id:
            from models.user import User
            author = User.objects(id=self.author_id).first()
            if author:
                data['author'] = author.to_dict()
        return data
