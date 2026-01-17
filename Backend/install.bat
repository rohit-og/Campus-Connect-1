@echo off
REM Installation script for Campus Connect AI Engine (Windows)

echo ========================================
echo Campus Connect AI Engine - Installation
echo ========================================

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed. Please install Python 3.8 or higher.
    pause
    exit /b 1
)

echo Python version:
python --version

REM Create virtual environment if it doesn't exist
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt

REM Create uploads directory
if not exist "uploads" (
    echo Creating uploads directory...
    mkdir uploads
)

echo.
echo ========================================
echo Installation completed successfully!
echo ========================================
echo.
echo To start the server, run:
echo   python start_server.py
echo   or
echo   python main.py
echo.
echo Then visit http://localhost:8000/docs for API documentation
echo.
pause


