@echo off
REM A-Player Hiring Suite Launch Script for Windows

echo ==================================================
echo   A-Player Hiring Suite
echo   Evidence-Based Hiring ^& Leadership Assessment
echo ==================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo X Python 3 is not installed. Please install Python 3.11 or later.
    pause
    exit /b 1
)

REM Check if we're in the correct directory
if not exist "backend" (
    echo X Error: Please run this script from the A_Player_Hiring_Suite directory
    pause
    exit /b 1
)

cd backend

REM Check if virtual environment exists
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
    echo Virtual environment created
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Check if dependencies are installed
if not exist "venv\installed.marker" (
    echo Installing dependencies...
    pip install -r requirements.txt
    echo. > venv\installed.marker
    echo Dependencies installed
)

REM Check if static files exist
if not exist "static\assets" (
    echo Warning: Frontend build not found in backend\static\
    echo    To build the frontend:
    echo    1. cd frontend
    echo    2. npm install
    echo    3. npm run build
    echo    4. xcopy /E /I dist ..\backend\static
    echo.
    echo    Running backend only (API will be available at http://localhost:8000/api/docs)
)

REM Start the server
echo.
echo Starting A-Player Hiring Suite...
echo Access at: http://localhost:8000
echo API docs: http://localhost:8000/api/docs
echo.
echo Press Ctrl+C to stop the server
echo.

python run.py
