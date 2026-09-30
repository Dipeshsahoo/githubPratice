# Quick Start Guide - Backend Server

## The Problem
Your frontend is running but showing connection errors because the backend Flask server is not running.

## Solution: Start the Backend

### Step 1: Open a NEW Terminal Window
Keep your frontend terminal running, and open a **second terminal window**.

### Step 2: Navigate to Backend Directory
```powershell
cd C:\Users\Dipesh Sahoo\OneDrive\Desktop\johnyAlumini\backend
```

### Step 3: Create .env File (if not exists)
Create a file named `.env` in the `backend` folder with this content:

```
FLASK_APP=app.py
FLASK_ENV=development
SECRET_KEY=dev-secret-key-change-in-production-12345
JWT_SECRET_KEY=dev-jwt-secret-key-change-in-production-12345
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/alumni_db
OPENAI_API_KEY=
CORS_ORIGINS=http://localhost:3000,http://localhost:5173
```

**Important:** Update `DATABASE_URL` with your PostgreSQL username and password if different.

### Step 4: Create Virtual Environment (First Time Only)
```powershell
python -m venv venv
```

### Step 5: Activate Virtual Environment
```powershell
.\venv\Scripts\Activate.ps1
```

If you get an execution policy error, run:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Step 6: Install Dependencies (First Time Only)
```powershell
pip install -r requirements.txt
```

### Step 7: Initialize Database (First Time Only)
Make sure PostgreSQL is running and the database exists:
```sql
CREATE DATABASE alumni_db;
```

Then run:
```powershell
python init_db.py
```

### Step 8: Start the Backend Server
```powershell
python app.py
```

You should see:
```
 * Running on http://0.0.0.0:5000
```

## Now Both Servers Are Running:
- ✅ Frontend: http://localhost:3000 (already running)
- ✅ Backend: http://localhost:5000 (just started)

The connection errors should disappear!

## Troubleshooting

### Database Connection Error?
- Make sure PostgreSQL is running
- Check your DATABASE_URL in .env matches your PostgreSQL setup
- Verify database exists: `psql -U postgres -l`

### Port 5000 Already in Use?
- Change port in `app.py` or use: `flask run --port 5001`
- Update `vite.config.js` proxy target to match

### Module Not Found?
- Make sure virtual environment is activated
- Run `pip install -r requirements.txt` again
