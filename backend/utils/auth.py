"""
Authentication utilities
"""

import secrets
from datetime import datetime, timedelta

def generate_verification_token():
    """Generate a secure verification token"""
    return secrets.token_urlsafe(32)

def verify_token(token, stored_token, expires_at=None):
    """Verify a token"""
    if not token or not stored_token:
        return False
    if token != stored_token:
        return False
    if expires_at and datetime.utcnow() > expires_at:
        return False
    return True
