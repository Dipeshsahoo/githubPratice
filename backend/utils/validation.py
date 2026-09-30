"""
Validation utilities
"""

import re
from email_validator import validate_email as validate_email_lib, EmailNotValidError

def validate_email(email):
    """Validate email address"""
    try:
        validate_email_lib(email)
        return True, None
    except EmailNotValidError as e:
        return False, str(e)

def validate_mobile(mobile):
    """Validate mobile number (basic validation)"""
    if not mobile:
        return False, "Mobile number is required"
    # Remove spaces and dashes
    mobile = re.sub(r'[\s-]', '', mobile)
    # Check if it's 10 digits (Indian format) or international format
    if re.match(r'^\+?[1-9]\d{9,14}$', mobile):
        return True, None
    return False, "Invalid mobile number format"
