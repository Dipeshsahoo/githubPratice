"""
Chatbot knowledge base model
"""

from datetime import datetime
from mongoengine import Document, fields

class ChatbotKnowledge(Document):
    """Chatbot knowledge base entry"""
    meta = {
        'collection': 'chatbot_knowledge',
        'indexes': ['category']
    }
    
    category = fields.StringField(max_length=100, required=True)
    question = fields.StringField(required=True)
    answer = fields.StringField(required=True)
    source_type = fields.StringField(max_length=50)
    source_id = fields.StringField()
    # Note: For vector embeddings, MongoDB supports array fields
    # embedding = fields.ListField(fields.FloatField())  # For future use
    created_at = fields.DateTimeField(default=datetime.utcnow)
    updated_at = fields.DateTimeField(default=datetime.utcnow)
    
    def save(self, *args, **kwargs):
        """Override save to update updated_at"""
        self.updated_at = datetime.utcnow()
        return super().save(*args, **kwargs)
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'id': str(self.id),
            'category': self.category,
            'question': self.question,
            'answer': self.answer,
            'source_type': self.source_type,
            'source_id': self.source_id,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
