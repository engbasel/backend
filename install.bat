@echo off
REM NeuroAid Backend - Quick Installation Script
REM This script will set up everything you need to run the backend

echo ============================================================
echo NeuroAid Backend - Quick Installation
echo ============================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH
    echo Please install Python 3.9 or higher from https://www.python.org/
    pause
    exit /b 1
)

echo [1/4] Python found:
python --version
echo.

REM Check if virtual environment exists
if not exist "venv" (
    echo [2/4] Creating virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo [ERROR] Failed to create virtual environment
        pause
        exit /b 1
    )
    echo Virtual environment created successfully
) else (
    echo [2/4] Virtual environment already exists
)
echo.

REM Activate virtual environment
echo [3/4] Activating virtual environment...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo [ERROR] Failed to activate virtual environment
    pause
    exit /b 1
)
echo.

REM Install requirements
echo [4/4] Installing all required packages...
echo This may take 5-10 minutes, please wait...
echo.
pip install --upgrade pip
pip install -r requirements.txt

if errorlevel 1 (
    echo.
    echo [ERROR] Failed to install some packages
    echo Please check the error messages above
    pause
    exit /b 1
)

echo.
echo ============================================================
echo Installation completed successfully!
echo ============================================================
echo.
echo Next steps:
echo 1. Copy .env.example to .env and configure it
echo 2. Run: python verify_installation.py (to verify)
echo 3. Run: python run_system.py (to start all services)
echo.
echo Or use: start_all_servers.bat
echo ============================================================
echo.

REM Run verification
echo Running verification script...
echo.
python verify_installation.py

pause
