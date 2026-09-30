"""
Gallery models
"""

from datetime import datetime
from mongoengine import Document, fields

class Album(Document):
    """Album model"""
    meta = {
        'collection': 'albums',
        'indexes': ['event_id', 'created_by']
    }
    
    title = fields.StringField(max_length=255, required=True)
    description = fields.StringField()
    event_id = fields.StringField()
    created_by = fields.StringField()
    created_at = fields.DateTimeField(default=datetime.utcnow)
    updated_at = fields.DateTimeField(default=datetime.utcnow)
    
    def save(self, *args, **kwargs):
        """Override save to update updated_at"""
        self.updated_at = datetime.utcnow()
        return super().save(*args, **kwargs)
    
    def to_dict(self, include_media=False):
        """Convert to dictionary"""
        media_count = None
        media_list = []
        if include_media:
            media_list = Media.objects(album_id=str(self.id))
            media_count = media_list.count()
        
        data = {
            'id': str(self.id),
            'title': self.title,
            'description': self.description,
            'event_id': self.event_id,
            'created_by': self.created_by,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'media_count': media_count
        }
        if include_media:
            data['media'] = [m.to_dict() for m in media_list]
        return data

class Media(Document):
    """Media file model"""
    meta = {
        'collection': 'media',
        'indexes': ['album_id']
    }
    
    album_id = fields.StringField(required=True)
    file_path = fields.StringField(max_length=255, required=True)
    file_type = fields.StringField(max_length=50, required=True)
    file_size = fields.IntField()
    thumbnail_path = fields.StringField(max_length=255)
    uploaded_by = fields.StringField()
    created_at = fields.DateTimeField(default=datetime.utcnow)
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'id': str(self.id),
            'album_id': self.album_id,
            'file_path': self.file_path,
            'file_type': self.file_type,
            'file_size': self.file_size,
            'thumbnail_path': self.thumbnail_path,
            'uploaded_by': self.uploaded_by,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
