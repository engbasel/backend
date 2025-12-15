@echo off
REM NeuroAid Backend System - Quick Start Script
REM This script starts all backend services using the orchestrator

echo.
echo ================================================================
echo          NeuroAid Backend System - Quick Start
echo ================================================================
echo.

REM Check if we're in the backend directory
if not exist "flask_server" (
    echo ERROR: Please run this script from the backend directory
    echo Current directory: %CD%
    pause
    exit /b 1
)

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8 or higher
    pause
    exit /b 1
)

echo Checking dependencies...
echo.

REM Install requirements if needed
pip show flask >nul 2>&1
if errorlevel 1 (
    echo Installing required packages...
    pip install -r requirements.txt
    echo.
)

echo.
echo ================================================================
echo   Starting NeuroAid Backend System...
echo ================================================================
echo.
echo Services that will start:
echo   - Main Flask Server     (Port 5000)
echo   - AI Chatbot Service    (Port 5001)
echo   - Stroke Assessment     (Port 5002)
echo   - API Gateway           (Port 8080)
echo.
echo Press CTRL+C to stop all services
echo ================================================================
echo.

REM Start the orchestrator
python run_system.py

pause
