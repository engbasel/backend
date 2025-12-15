@echo off
title NeuroAid Flask Backend Setup
color 0A

echo.
echo ========================================
echo   NeuroAid Flask Backend Setup
echo ========================================
echo.

REM Check Python
echo [1/3] Checking Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed!
    echo Please install Python from https://www.python.org/
    pause
    exit /b 1
)
echo ✓ Python is installed

REM Create virtual environment
echo.
echo [2/3] Creating virtual environment...
if not exist "venv\" (
    python -m venv venv
    echo ✓ Virtual environment created
) else (
    echo ✓ Virtual environment already exists
)

REM Install dependencies
echo.
echo [3/3] Installing dependencies...
call venv\Scripts\activate.bat
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)
echo ✓ Dependencies installed

REM Copy .env.example to .env if not exists
if not exist ".env" (
    copy .env.example .env
    echo ✓ Created .env file from .env.example
)

echo.
echo ========================================
echo   Setup Complete!
echo ========================================
echo.
echo To start the server, run: start_server.bat
echo.
pause
