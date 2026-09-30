# Alumni Website - Platinum Jubilee

A production-ready Alumni Website for a school's Platinum Jubilee celebration. Built with React frontend, Flask backend, PostgreSQL database, and JWT authentication.

## Features

- 🔐 **Authentication**: JWT-based login, email/mobile verification, profile completion
- 👥 **Alumni Directory**: Search by name, batch, profession, location with public/private profiles
- 📅 **Events & Jubilee**: Event management, registration, QR code check-in, countdown timer
- 📰 **News & Announcements**: Admin-posted announcements with sharing
- 📸 **Gallery & Media**: Photo/video albums organized by events
- 🤝 **Mentorship**: Alumni mentorship availability posts
- 💼 **Jobs & Internships**: Job postings and application tracking
- 💝 **Donations**: Donation form with status tracking
- 👨‍💼 **Admin Dashboard**: User management, content moderation, statistics
- 🤖 **AI Chatbot**: Retrieval-based chatbot answering website-related queries
- 📱 **WhatsApp Ready**: API endpoint for future WhatsApp integration

## Tech Stack

### Frontend
- React 18
- Tailwind CSS
- React Router
- Axios
- React Query
- Vite

### Backend
- Flask
- Flask-SQLAlchemy
- Flask-JWT-Extended
- PostgreSQL
- OpenAI API (for chatbot)

## Project Structure

```
johnyAlumini/
├── backend/
│   ├── app.py                 # Flask application entry point
│   ├── config.py              # Configuration
│   ├── extensions.py          # Flask extensions
│   ├── requirements.txt       # Python dependencies
│   ├── models/                # Database models
│   ├── routes/                # API routes
│   ├── utils/                 # Utility functions
│   └── middleware/            # Auth middleware
├── frontend/
│   ├── src/
│   │   ├── components/        # React components
│   │   ├── pages/             # Page components
│   │   ├── contexts/          # React contexts
│   │   ├── services/          # API services
│   │   └── App.jsx            # Main app component
│   ├── package.json
│   └── vite.config.js
├── ARCHITECTURE.md            # System architecture
├── DATABASE_SCHEMA.md         # Database schema
└── README.md                  # This file
```

## Setup Instructions

### Prerequisites

- Python 3.9+
- Node.js 18+
- PostgreSQL 12+
- OpenAI API key (for chatbot)

### Backend Setup

1. **Navigate to backend directory:**
   ```bash
   cd backend
   ```

2. **Create virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up PostgreSQL database:**
   ```sql
   CREATE DATABASE alumni_db;
   ```

5. **Create `.env` file:**
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env` and set:
   - `DATABASE_URL`: PostgreSQL connection string
   - `SECRET_KEY`: Flask secret key
   - `JWT_SECRET_KEY`: JWT secret key
   - `OPENAI_API_KEY`: OpenAI API key (for chatbot)

6. **Run database migrations:**
   ```bash
   flask db init
   flask db migrate -m "Initial migration"
   flask db upgrade
   ```

7. **Create upload directories:**
   ```bash
   mkdir -p uploads/profiles uploads/media uploads/resumes
   ```

8. **Run the Flask server:**
   ```bash
   python app.py
   ```

   Backend will run on `http://localhost:5000`

### Frontend Setup

1. **Navigate to frontend directory:**
   ```bash
   cd frontend
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Start development server:**
   ```bash
   npm run dev
   ```

   Frontend will run on `http://localhost:3000`

### Creating Admin User

To create an admin user, you can use Python shell:

```python
from app import create_app, db
from models.user import User, Profile

app = create_app()
with app.app_context():
    admin = User(
        email='admin@example.com',
        role='admin',
        is_verified=True,
        is_approved=True
    )
    admin.set_password('admin123')
    db.session.add(admin)
    
    profile = Profile(
        user_id=admin.id,
        first_name='Admin',
        last_name='User',
        is_profile_complete=True
    )
    db.session.add(profile)
    db.session.commit()
```

## API Documentation

See [API_DOCUMENTATION.md](API_DOCUMENTATION.md) for detailed API endpoints.

### Base URL
```
http://localhost:5000/api/v1
```

### Authentication
Most endpoints require JWT authentication. Include token in header:
```
Authorization: Bearer <access_token>
```

## Environment Variables

### Backend (.env)
- `FLASK_APP`: Flask application (default: app.py)
- `FLASK_ENV`: Environment (development/production)
- `SECRET_KEY`: Flask secret key
- `JWT_SECRET_KEY`: JWT secret key
- `DATABASE_URL`: PostgreSQL connection string
- `OPENAI_API_KEY`: OpenAI API key
- `UPLOAD_FOLDER`: Upload directory path
- `CORS_ORIGINS`: Allowed CORS origins (comma-separated)

## Features Overview

### Authentication
- Alumni registration with email/mobile
- Email/mobile verification
- JWT-based authentication
- Password reset functionality
- Profile completion after first login

### Alumni Directory
- Search by name, batch year, profession, location
- Public profile view
- Private contact information (logged-in users only)
- Pagination support

### Events
- Create and manage events (admin)
- Event registration
- QR code generation for check-in
- Platinum Jubilee special events
- Registration deadline and capacity management

### News & Announcements
- Admin-posted announcements
- Categorization
- Publishing workflow

### Gallery
- Create albums
- Upload photos/videos
- Event-based organization
- Thumbnail generation

### Mentorship
- Post mentorship availability
- Expertise area filtering
- Availability status
- Admin approval workflow

### Jobs
- Job/internship postings
- Application tracking
- Resume upload
- Status management

### Donations
- Donation form
- Status tracking (pending/approved/rejected/completed)
- Payment method recording
- Admin processing

### Admin Dashboard
- User management and approval
- Content moderation
- Statistics and analytics
- Event management

### AI Chatbot
- Retrieval-based responses
- Knowledge base from website data
- Answers questions about:
  - Registration process
  - Event joining
  - Directory usage
  - Jubilee schedule
  - Donation information
- WhatsApp API endpoint ready

## Deployment

### Backend Deployment

1. Set production environment variables
2. Use production WSGI server (Gunicorn):
   ```bash
   gunicorn -w 4 -b 0.0.0.0:5000 app:app
   ```
3. Set up reverse proxy (Nginx)
4. Configure SSL/TLS certificates

### Frontend Deployment

1. Build production bundle:
   ```bash
   npm run build
   ```
2. Serve `dist/` directory with Nginx or similar
3. Configure API proxy

## Security Considerations

- Password hashing with bcrypt
- JWT token expiration
- Input validation
- SQL injection prevention (ORM)
- File upload validation
- CORS configuration
- Role-based access control

## Contributing

1. Fork the repository
2. Create feature branch
3. Commit changes
4. Push to branch
5. Create Pull Request

## License

This project is proprietary software for the school's Platinum Jubilee celebration.

## Support

For issues and questions, please contact the development team.
