"""
Gallery routes
"""

from flask import Blueprint, request, jsonify
from extensions import db
from models.gallery import Album, Media
from middleware.auth import admin_required, alumni_required
from flask_jwt_extended import get_jwt_identity
from utils.file_upload import allowed_file, save_uploaded_file
from werkzeug.utils import secure_filename

gallery_bp = Blueprint('gallery', __name__)

@gallery_bp.route('', methods=['GET'])
def list_albums():
    """List albums"""
    event_id = request.args.get('event_id', type=int)
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    
    query = Album.query
    
    if event_id:
        query = query.filter(Album.event_id == event_id)
    
    query = query.order_by(Album.created_at.desc())
    
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    
    albums = [album.to_dict(include_media=False) for album in pagination.items]
    
    return jsonify({
        'albums': albums,
        'total': pagination.total,
        'page': page,
        'per_page': per_page,
        'pages': pagination.pages
    }), 200

@gallery_bp.route('/<int:album_id>', methods=['GET'])
def get_album(album_id):
    """Get album with media"""
    album = Album.query.get_or_404(album_id)
    return jsonify(album.to_dict(include_media=True)), 200

@gallery_bp.route('', methods=['POST'])
@admin_required
def create_album():
    """Create album (admin only)"""
    data = request.get_json()
    
    if 'title' not in data:
        return jsonify({'error': 'Title is required'}), 400
    
    album = Album(
        title=data['title'],
        description=data.get('description'),
        event_id=data.get('event_id'),
        created_by=get_jwt_identity()
    )
    
    db.session.add(album)
    db.session.commit()
    
    return jsonify({
        'message': 'Album created successfully',
        'album': album.to_dict()
    }), 201

@gallery_bp.route('/<int:album_id>/upload', methods=['POST'])
@admin_required
def upload_media(album_id):
    """Upload media to album (admin only)"""
    album = Album.query.get_or_404(album_id)
    
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if not allowed_file(file.filename):
        return jsonify({'error': 'File type not allowed'}), 400
    
    # Save file
    result = save_uploaded_file(file, 'media')
    if not result:
        return jsonify({'error': 'Failed to save file'}), 500
    
    # Determine file type
    ext = file.filename.rsplit('.', 1)[1].lower()
    file_type = 'image' if ext in ['jpg', 'jpeg', 'png', 'gif'] else 'video'
    
    # Create media record
    media = Media(
        album_id=album_id,
        file_path=result['file_path'],
        file_type=file_type,
        file_size=result.get('file_size'),
        thumbnail_path=result.get('thumbnail_path'),
        uploaded_by=get_jwt_identity()
    )
    
    db.session.add(media)
    db.session.commit()
    
    return jsonify({
        'message': 'Media uploaded successfully',
        'media': media.to_dict()
    }), 201

@gallery_bp.route('/<int:album_id>', methods=['DELETE'])
@admin_required
def delete_album(album_id):
    """Delete album (admin only)"""
    album = Album.query.get_or_404(album_id)
    db.session.delete(album)
    db.session.commit()
    
    return jsonify({'message': 'Album deleted successfully'}), 200
