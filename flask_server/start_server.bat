@echo off
title NeuroAid Flask Backend Server
color 0A

echo.
echo ========================================
echo   Starting NeuroAid Flask Backend
echo ========================================
echo.

REM Check if virtual environment exists
if not exist "venv\" (
    echo ERROR: Virtual environment not found!
    echo Please run setup.bat first
    pause
    exit /b 1
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Check if .env exists
if not exist ".env" (
    echo Creating .env from .env.example...
    copy .env.example .env
)

REM Start Flask server
echo Starting Flask server...
echo.
python app.py

pause
