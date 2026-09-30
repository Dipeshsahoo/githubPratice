# Quick Start Guide

## Prerequisites

- ✅ MongoDB installed and running
- ✅ Python 3.9+ installed
- ✅ Node.js 18+ installed

## Option 1: Use the Startup Script (Easiest)

**Windows:**
```powershell
.\start_app.ps1
```

This will:
- Check MongoDB status
- Create `.env` file if needed
- Start backend in a new window
- Start frontend in a new window

## Option 2: Manual Start

### Terminal 1 - Backend

```powershell
cd backend

# Activate virtual environment (if exists)
.\venv\Scripts\Activate.ps1

# Install dependencies (first time only)
pip install -r requirements.txt

# Create .env file with:
# MONGODB_URI=mongodb://localhost:27017/alumni_db
# SECRET_KEY=dev-secret-key
# JWT_SECRET_KEY=dev-jwt-secret-key

# Start server
python app.py
```

### Terminal 2 - Frontend

```powershell
cd frontend

# Install dependencies (first time only)
npm install

# Start server
npm run dev
```

## Access the Application

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:5000
- **API Health Check**: http://localhost:5000/

## First Time Setup

1. **Create admin user:**
   ```powershell
   cd backend
   python init_db.py create_admin admin@example.com admin123
   ```

2. **Register a new user** via the frontend or API

3. **Login** and start using the application

## Troubleshooting

### MongoDB Connection Error
- Ensure MongoDB is running: `mongosh` should connect
- Check `.env` file has correct `MONGODB_URI`

### Port Already in Use
- Backend: Change port in `app.py` (line 57)
- Frontend: Vite will suggest another port automatically

### Module Not Found
- Backend: Run `pip install -r requirements.txt`
- Frontend: Run `npm install`

### Route Errors
- Some routes may still need MongoDB conversion
- Check `MONGODB_CONVERSION_STATUS.md` for status
