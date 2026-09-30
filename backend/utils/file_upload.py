"""
File upload utilities
"""

import os
from werkzeug.utils import secure_filename
from flask import current_app
from PIL import Image

def allowed_file(filename):
    """Check if file extension is allowed"""
    if '.' not in filename:
        return False
    ext = filename.rsplit('.', 1)[1].lower()
    return ext in current_app.config['ALLOWED_EXTENSIONS']

def save_uploaded_file(file, subfolder=''):
    """Save uploaded file and return path"""
    if not file or not allowed_file(file.filename):
        return None
    
    filename = secure_filename(file.filename)
    timestamp = str(int(os.path.getmtime(__file__) * 1000))
    name, ext = os.path.splitext(filename)
    unique_filename = f"{name}_{timestamp}{ext}"
    
    upload_folder = current_app.config['UPLOAD_FOLDER']
    if subfolder:
        upload_folder = os.path.join(upload_folder, subfolder)
    
    os.makedirs(upload_folder, exist_ok=True)
    filepath = os.path.join(upload_folder, unique_filename)
    file.save(filepath)
    
    # Generate thumbnail for images
    thumbnail_path = None
    if ext.lower() in ['.jpg', '.jpeg', '.png', '.gif']:
        try:
            img = Image.open(filepath)
            img.thumbnail((300, 300))
            thumbnail_filename = f"{name}_{timestamp}_thumb{ext}"
            thumbnail_path = os.path.join(upload_folder, thumbnail_filename)
            img.save(thumbnail_path)
        except Exception:
            pass
    
    return {
        'file_path': filepath,
        'filename': unique_filename,
        'thumbnail_path': thumbnail_path
    }
