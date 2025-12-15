@echo off
echo ========================================
echo Starting NeuroAid AI Services
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8 or higher
    pause
    exit /b 1
)

echo [1/3] Starting Chatbot Service on port 5001...
start "NeuroAid Chatbot" cmd /k "cd chatbot && python app.py"
timeout /t 2 >nul

echo [2/3] Starting Stroke Assessment Service on port 5002...
start "NeuroAid Stroke Assessment" cmd /k "cd stroke_assessment && python app.py"
timeout /t 2 >nul

echo [3/3] Starting Stroke Image Analysis Service on port 5003...
start "NeuroAid Image Analysis" cmd /k "cd stroke_image && python app.py"
timeout /t 2 >nul

echo.
echo ========================================
echo All AI Services Started!
echo ========================================
echo.
echo Chatbot:           http://localhost:5001
echo Stroke Assessment: http://localhost:5002
echo Image Analysis:    http://localhost:5003
echo.
echo Press any key to open health check in browser...
pause >nul

start http://localhost:5001/health
start http://localhost:5002/health
start http://localhost:5003/health

echo.
echo Services are running in separate windows.
echo Close those windows to stop the services.
echo.
pause
