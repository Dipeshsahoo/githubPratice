@echo off
echo Starting Alumni Website Backend Server...
echo.

REM Check if virtual environment exists
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies if needed
if not exist "venv\Lib\site-packages\flask" (
    echo Installing dependencies...
    pip install -r requirements.txt
)

REM Check if .env exists
if not exist ".env" (
    echo.
    echo WARNING: .env file not found!
    echo Please create .env file with your database configuration.
    echo See START_BACKEND.md for details.
    echo.
    pause
)

REM Start the server
echo.
echo Starting Flask server...
echo Backend will run on http://localhost:5000
echo.
python app.py

pause
