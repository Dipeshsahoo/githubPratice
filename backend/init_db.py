"""
Database initialization script
Run this to create indexes and optionally create an admin user
Note: MongoDB doesn't require table creation, but we can create indexes
"""

from app import create_app
from models.user import User, Profile

def init_database():
    """Initialize database indexes"""
    app = create_app()
    with app.app_context():
        print("MongoDB connection established!")
        print("Note: MongoDB is schema-less, no tables to create.")
        print("Indexes are created automatically when models are defined.")

def create_admin(email, password, first_name="Admin", last_name="User"):
    """Create an admin user"""
    app = create_app()
    with app.app_context():
        # Check if admin exists
        existing = User.objects(email=email).first()
        if existing:
            print(f"User with email {email} already exists!")
            return
        
        # Create admin user
        admin = User(
            email=email,
            role='admin',
            is_verified=True,
            is_approved=True
        )
        admin.set_password(password)
        admin.save()
        
        # Create profile
        profile = Profile(
            user_id=str(admin.id),
            first_name=first_name,
            last_name=last_name,
            is_profile_complete=True
        )
        profile.save()
        
        print(f"Admin user created successfully!")
        print(f"Email: {email}")
        print(f"Password: {password}")

if __name__ == '__main__':
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == 'create_admin':
        if len(sys.argv) < 4:
            print("Usage: python init_db.py create_admin <email> <password> [first_name] [last_name]")
            sys.exit(1)
        
        email = sys.argv[2]
        password = sys.argv[3]
        first_name = sys.argv[4] if len(sys.argv) > 4 else "Admin"
        last_name = sys.argv[5] if len(sys.argv) > 5 else "User"
        
        init_database()
        create_admin(email, password, first_name, last_name)
    else:
        init_database()
        print("\nTo create an admin user, run:")
        print("python init_db.py create_admin <email> <password>")
