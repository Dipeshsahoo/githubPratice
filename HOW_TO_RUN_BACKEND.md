# How to Run the Backend

## Prerequisites

1. **MongoDB must be running** on port 27017
2. **Python 3.9+** installed
3. **Virtual environment** set up (or create one)

## Step-by-Step Instructions

### Step 1: Navigate to Backend Directory

```powershell
cd backend
```

### Step 2: Activate Virtual Environment

```powershell
.\venv\Scripts\Activate.ps1
```

If you get an execution policy error:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Step 3: Install Dependencies (First Time Only)

```powershell
pip install -r requirements.txt
```

### Step 4: Create .env File (If Not Exists)

Create a file named `.env` in the `backend` folder with:

```env
MONGODB_URI=mongodb://localhost:27017/alumni_db
SECRET_KEY=dev-secret-key-change-in-production-12345
JWT_SECRET_KEY=dev-jwt-secret-key-change-in-production-12345
OPENAI_API_KEY=
CORS_ORIGINS=http://localhost:3000,http://localhost:5173
```

### Step 5: Run the Backend

**Method 1: Using app.py (Development)**
```powershell
python app.py
```

**Method 2: Using run.py (Production)**
```powershell
python run.py
```

**Method 3: Using Flask CLI**
```powershell
flask run
```

**Method 4: Using the startup script**
```powershell
.\start_backend.ps1
```

## Expected Output

You should see:
```
✓ MongoDB connection established
🚀 Starting Flask server on http://localhost:5000
 * Running on http://0.0.0.0:5000
 * Debug mode: on
```

## Verify It's Running

Open your browser and go to:
- **Health Check**: http://localhost:5000/
- **API Base**: http://localhost:5000/api/v1

You should see:
```json
{"status": "ok", "message": "Alumni Website API"}
```

## Troubleshooting

### MongoDB Connection Error
- Make sure MongoDB is running: `mongosh` should connect
- Check `.env` file has correct `MONGODB_URI`
- Verify MongoDB service: `Get-Service -Name MongoDB`

### Module Not Found Error
- Activate virtual environment: `.\venv\Scripts\Activate.ps1`
- Install dependencies: `pip install -r requirements.txt`

### Port Already in Use
- Change port in `app.py` line 65: `port=5001`
- Or kill the process using port 5000

### Import Errors
- Make sure you're in the `backend` directory
- Virtual environment should be activated
- All dependencies installed

## Quick Command Summary

```powershell
# Complete setup and run
cd backend
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt  # First time only
python app.py
```

## Stop the Server

Press `Ctrl + C` in the terminal where the server is running.
