"""
Alumni Website - Flask Backend Application
Main application entry point
"""

from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from mongoengine import connect, disconnect
from dotenv import load_dotenv
import os

from config import Config
from routes import register_blueprints

# Load environment variables
load_dotenv()

def create_app(config_class=Config):
    """Application factory pattern"""
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Initialize MongoDB connection
    try:
        if app.config.get('MONGODB_URI'):
            connect(host=app.config['MONGODB_URI'])
        else:
            connect(
                db=app.config['MONGODB_DB'],
                host=app.config['MONGODB_HOST'],
                port=app.config['MONGODB_PORT'],
                username=app.config.get('MONGODB_USERNAME'),
                password=app.config.get('MONGODB_PASSWORD'),
                authentication_source='admin' if app.config.get('MONGODB_USERNAME') else None
            )
        print("✓ MongoDB connection established")
    except Exception as e:
        print(f"⚠ Warning: Could not connect to MongoDB: {e}")
        print("  The server will start, but database operations will fail.")
        print("  Please ensure MongoDB is running and MONGODB_URI is correct in .env")
    
    # Initialize extensions
    JWTManager(app)
    CORS(app, origins=app.config['CORS_ORIGINS'], supports_credentials=True)
    
    # Register blueprints
    register_blueprints(app)
    
    # Create upload directories
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], 'profiles'), exist_ok=True)
    os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], 'media'), exist_ok=True)
    os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], 'resumes'), exist_ok=True)
    
    @app.route('/')
    def health_check():
        return {'status': 'ok', 'message': 'Alumni Website API'}, 200
    
    return app

if __name__ == '__main__':
    app = create_app()
    print("\n🚀 Starting Flask server on http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)
