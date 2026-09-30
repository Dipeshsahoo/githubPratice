"""
Route blueprints registration
"""

from flask import Blueprint

def register_blueprints(app):
    """Register all blueprints"""
    from .auth import auth_bp
    from .alumni import alumni_bp
    from .events import events_bp
    from .news import news_bp
    from .gallery import gallery_bp
    from .mentorship import mentorship_bp
    from .jobs import jobs_bp
    from .donations import donations_bp
    from .admin import admin_bp
    from .chatbot import chatbot_bp
    
    app.register_blueprint(auth_bp, url_prefix='/api/v1/auth')
    app.register_blueprint(alumni_bp, url_prefix='/api/v1/alumni')
    app.register_blueprint(events_bp, url_prefix='/api/v1/events')
    app.register_blueprint(news_bp, url_prefix='/api/v1/news')
    app.register_blueprint(gallery_bp, url_prefix='/api/v1/gallery')
    app.register_blueprint(mentorship_bp, url_prefix='/api/v1/mentorship')
    app.register_blueprint(jobs_bp, url_prefix='/api/v1/jobs')
    app.register_blueprint(donations_bp, url_prefix='/api/v1/donations')
    app.register_blueprint(admin_bp, url_prefix='/api/v1/admin')
    app.register_blueprint(chatbot_bp, url_prefix='/api/v1/chatbot')
