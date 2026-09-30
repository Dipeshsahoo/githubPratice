# Quick Setup Guide

## Prerequisites Check

- [ ] Python 3.9+ installed
- [ ] Node.js 18+ installed
- [ ] PostgreSQL 12+ installed and running
- [ ] OpenAI API key (for chatbot feature)

## Step-by-Step Setup

### 1. Database Setup

```bash
# Create PostgreSQL database
createdb alumni_db

# Or using psql:
psql -U postgres
CREATE DATABASE alumni_db;
\q
```

### 2. Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file (copy from .env.example)
# Edit .env and set:
# - DATABASE_URL=postgresql://user:password@localhost:5432/alumni_db
# - SECRET_KEY=your-secret-key
# - JWT_SECRET_KEY=your-jwt-secret-key
# - OPENAI_API_KEY=your-openai-api-key

# Initialize database
python init_db.py

# Create admin user
python init_db.py create_admin admin@example.com admin123

# Run Flask server
python app.py
```

Backend should be running on `http://localhost:5000`

### 3. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

Frontend should be running on `http://localhost:3000`

### 4. Verify Setup

1. Open `http://localhost:3000` in browser
2. You should see the homepage
3. Try registering a new account
4. Login with admin credentials: `admin@example.com` / `admin123`
5. Access admin dashboard at `/admin`

## Common Issues

### Database Connection Error
- Check PostgreSQL is running: `pg_isready`
- Verify DATABASE_URL in .env file
- Ensure database exists: `psql -l | grep alumni_db`

### Port Already in Use
- Backend: Change port in `app.py` or use environment variable
- Frontend: Change port in `vite.config.js`

### Module Not Found
- Ensure virtual environment is activated
- Run `pip install -r requirements.txt` again
- Check Python path

### OpenAI Chatbot Not Working
- Verify OPENAI_API_KEY in .env
- Check API key is valid and has credits
- Chatbot will show fallback message if not configured

## Next Steps

1. Customize the homepage content
2. Add your school's branding
3. Configure email settings for verification (optional)
4. Set up production environment variables
5. Deploy to production server

## Production Deployment

See README.md for production deployment instructions.
