# PowerShell script to start the backend server

Write-Host "Starting Alumni Website Backend Server..." -ForegroundColor Cyan
Write-Host ""

# Check if virtual environment exists
if (-not (Test-Path "venv")) {
    Write-Host "Creating virtual environment..." -ForegroundColor Yellow
    python -m venv venv
}

# Activate virtual environment
Write-Host "Activating virtual environment..." -ForegroundColor Yellow
& .\venv\Scripts\Activate.ps1

# Install dependencies if needed
if (-not (Test-Path "venv\Lib\site-packages\flask")) {
    Write-Host "Installing dependencies..." -ForegroundColor Yellow
    pip install -r requirements.txt
}

# Check if .env exists
if (-not (Test-Path ".env")) {
    Write-Host ""
    Write-Host "WARNING: .env file not found!" -ForegroundColor Red
    Write-Host "Please create .env file with your database configuration." -ForegroundColor Yellow
    Write-Host "See START_BACKEND.md for details." -ForegroundColor Yellow
    Write-Host ""
    Read-Host "Press Enter to continue anyway"
}

# Start the server
Write-Host ""
Write-Host "Starting Flask server..." -ForegroundColor Green
Write-Host "Backend will run on http://localhost:5000" -ForegroundColor Green
Write-Host ""
python app.py
