"""
News and announcements routes
"""

from flask import Blueprint, request, jsonify
from extensions import db
from models.news import News
from middleware.auth import admin_required
from flask_jwt_extended import get_jwt_identity
from datetime import datetime

news_bp = Blueprint('news', __name__)

@news_bp.route('', methods=['GET'])
def list_news():
    """List news and announcements"""
    category = request.args.get('category')
    published_only = request.args.get('published_only', 'true').lower() == 'true'
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    
    query = News.query
    
    if published_only:
        query = query.filter(News.is_published == True)
    
    if category:
        query = query.filter(News.category == category)
    
    query = query.order_by(News.published_at.desc() if published_only else News.created_at.desc())
    
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    
    news_list = [news.to_dict(include_author=True) for news in pagination.items]
    
    return jsonify({
        'news': news_list,
        'total': pagination.total,
        'page': page,
        'per_page': per_page,
        'pages': pagination.pages
    }), 200

@news_bp.route('/<int:news_id>', methods=['GET'])
def get_news(news_id):
    """Get news article"""
    news = News.query.get_or_404(news_id)
    
    # Only show published news to non-admins
    current_user_id = None
    try:
        from flask_jwt_extended import verify_jwt_in_request
        verify_jwt_in_request(optional=True)
        current_user_id = get_jwt_identity()
        from models.user import User
        user = User.query.get(current_user_id) if current_user_id else None
        if not user or user.role != 'admin':
            if not news.is_published:
                return jsonify({'error': 'News not found'}), 404
    except:
        if not news.is_published:
            return jsonify({'error': 'News not found'}), 404
    
    return jsonify(news.to_dict(include_author=True)), 200

@news_bp.route('', methods=['POST'])
@admin_required
def create_news():
    """Create news (admin only)"""
    data = request.get_json()
    
    required_fields = ['title', 'content']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'{field} is required'}), 400
    
    news = News(
        title=data['title'],
        content=data['content'],
        category=data.get('category'),
        author_id=get_jwt_identity(),
        is_published=data.get('is_published', False),
        published_at=datetime.utcnow() if data.get('is_published', False) else None
    )
    
    db.session.add(news)
    db.session.commit()
    
    return jsonify({
        'message': 'News created successfully',
        'news': news.to_dict()
    }), 201

@news_bp.route('/<int:news_id>', methods=['PUT'])
@admin_required
def update_news(news_id):
    """Update news (admin only)"""
    news = News.query.get_or_404(news_id)
    data = request.get_json()
    
    if 'title' in data:
        news.title = data['title']
    if 'content' in data:
        news.content = data['content']
    if 'category' in data:
        news.category = data['category']
    if 'is_published' in data:
        news.is_published = data['is_published']
        if data['is_published'] and not news.published_at:
            news.published_at = datetime.utcnow()
    
    db.session.commit()
    
    return jsonify({
        'message': 'News updated successfully',
        'news': news.to_dict()
    }), 200

@news_bp.route('/<int:news_id>', methods=['DELETE'])
@admin_required
def delete_news(news_id):
    """Delete news (admin only)"""
    news = News.query.get_or_404(news_id)
    db.session.delete(news)
    db.session.commit()
    
    return jsonify({'message': 'News deleted successfully'}), 200
