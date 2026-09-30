# PowerShell script to start the Alumni Website application

Write-Host "=== Alumni Website Startup ===" -ForegroundColor Cyan
Write-Host ""

# Check MongoDB
Write-Host "Checking MongoDB..." -ForegroundColor Yellow
try {
    $mongoService = Get-Service -Name MongoDB -ErrorAction SilentlyContinue
    if ($mongoService -and $mongoService.Status -eq 'Running') {
        Write-Host "[OK] MongoDB is running" -ForegroundColor Green
    } else {
        Write-Host "[WARNING] MongoDB service not found or not running" -ForegroundColor Red
        Write-Host "  Please start MongoDB manually" -ForegroundColor Yellow
        Write-Host "  Or install MongoDB from: https://www.mongodb.com/try/download/community" -ForegroundColor Yellow
    }
} catch {
    Write-Host "[WARNING] Could not check MongoDB status" -ForegroundColor Yellow
    Write-Host "  Make sure MongoDB is installed and running" -ForegroundColor Yellow
}

Write-Host ""

# Start Backend
Write-Host "Starting Backend Server..." -ForegroundColor Yellow
$backendPath = Join-Path $PSScriptRoot "backend"
Set-Location $backendPath

# Check if .env exists
if (-not (Test-Path ".env")) {
    Write-Host "[WARNING] .env file not found!" -ForegroundColor Red
    Write-Host "  Creating .env file with default values..." -ForegroundColor Yellow
    $envContent = "MONGODB_URI=mongodb://localhost:27017/alumni_db`nSECRET_KEY=dev-secret-key-change-in-production-12345`nJWT_SECRET_KEY=dev-jwt-secret-key-change-in-production-12345`nOPENAI_API_KEY=`nCORS_ORIGINS=http://localhost:3000,http://localhost:5173"
    $envContent | Out-File -FilePath ".env" -Encoding utf8 -NoNewline
    Write-Host "  [OK] .env file created" -ForegroundColor Green
}

# Activate venv if exists
if (Test-Path "venv\Scripts\Activate.ps1") {
    Write-Host "Activating virtual environment..." -ForegroundColor Yellow
    & .\venv\Scripts\Activate.ps1
}

# Start backend in new window
Write-Host "Starting Flask backend..." -ForegroundColor Green
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$backendPath'; if (Test-Path venv\Scripts\Activate.ps1) { .\venv\Scripts\Activate.ps1 }; python app.py"

Write-Host ""

# Start Frontend
Write-Host "Starting Frontend Server..." -ForegroundColor Yellow
$frontendPath = Join-Path $PSScriptRoot "frontend"
Set-Location $frontendPath

# Check if node_modules exists
if (-not (Test-Path "node_modules")) {
    Write-Host "Installing frontend dependencies..." -ForegroundColor Yellow
    npm install
}

# Start frontend in new window
Write-Host "Starting React frontend..." -ForegroundColor Green
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$frontendPath'; npm run dev"

Write-Host ""
Write-Host "=== Application Starting ===" -ForegroundColor Cyan
Write-Host "Backend: http://localhost:5000" -ForegroundColor Green
Write-Host "Frontend: http://localhost:3000" -ForegroundColor Green
Write-Host ""
Write-Host "Two new terminal windows have opened:" -ForegroundColor Yellow
Write-Host "  1. Backend server (Flask)" -ForegroundColor White
Write-Host "  2. Frontend server (Vite)" -ForegroundColor White
Write-Host ""
Write-Host "Press any key to exit this script (servers will continue running)..." -ForegroundColor Yellow
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
