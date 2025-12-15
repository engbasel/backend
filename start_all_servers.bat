@echo off
setlocal enabledelayedexpansion
title NeuroAid - Complete System Startup
color 0B

REM ========================================
REM   NeuroAid Complete System Startup
REM ========================================

echo.
echo ╔════════════════════════════════════════════════════════════════╗
echo ║         NeuroAid - Complete System Startup Manager            ║
echo ╚════════════════════════════════════════════════════════════════╝
echo.

REM ========================================
REM   Step 1: Check Prerequisites
REM ========================================

echo [1/5] Checking Prerequisites...
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo.

REM Check Python
echo Checking Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ ERROR: Python is not installed!
    echo    Please install Python from https://www.python.org/
    pause
    exit /b 1
)
for /f "tokens=*" %%i in ('python --version') do set PYTHON_VERSION=%%i
echo ✅ %PYTHON_VERSION% is installed
echo.

REM Check pip
echo Checking pip...
pip --version >nul 2>&1
if errorlevel 1 (
    echo ❌ ERROR: pip is not installed!
    pause
    exit /b 1
)
for /f "tokens=*" %%i in ('pip --version') do set PIP_VERSION=%%i
echo ✅ pip is installed
echo.

echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo.

REM ========================================
REM   Step 2: Check Dependencies
REM ========================================

echo [2/5] Checking Python Dependencies...
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo.

REM Check Flask Server dependencies
echo Checking Flask Server dependencies...
if not exist "flask_server\venv\" (
    echo ⚠️  Flask Server virtual environment not found
    echo    Creating virtual environment...
    cd flask_server
    python -m venv venv
    call venv\Scripts\activate
    pip install -r requirements.txt
    deactivate
    cd ..
    echo ✅ Flask Server dependencies installed
) else (
    echo ✅ Flask Server dependencies ready
)
echo.

REM Check AI Services dependencies
echo Checking AI Services dependencies...

REM Chatbot
if not exist "ai_services\chatbot\venv\" (
    echo ⚠️  Chatbot virtual environment not found
    echo    Installing Chatbot dependencies...
    cd ai_services\chatbot
    python -m venv venv
    call venv\Scripts\activate
    pip install flask flask-cors
    deactivate
    cd ..\..
    echo ✅ Chatbot dependencies installed
) else (
    echo ✅ Chatbot dependencies ready
)
echo.

REM Stroke Assessment
if not exist "ai_services\stroke_assessment\venv\" (
    echo ⚠️  Stroke Assessment virtual environment not found
    echo    Installing Stroke Assessment dependencies...
    cd ai_services\stroke_assessment
    python -m venv venv
    call venv\Scripts\activate
    pip install flask flask-cors numpy scikit-learn
    deactivate
    cd ..\..
    echo ✅ Stroke Assessment dependencies installed
) else (
    echo ✅ Stroke Assessment dependencies ready
)
echo.

REM Stroke Image Analysis
if not exist "ai_services\stroke_image\venv\" (
    echo ⚠️  Stroke Image Analysis virtual environment not found
    echo    Installing Stroke Image dependencies...
    cd ai_services\stroke_image
    python -m venv venv
    call venv\Scripts\activate
    pip install -r requirements.txt
    deactivate
    cd ..\..
    echo ✅ Stroke Image Analysis dependencies installed
) else (
    echo ✅ Stroke Image Analysis dependencies ready
)
echo.

echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo.

REM ========================================
REM   Step 3: Start Servers
REM ========================================

echo [3/5] Starting All Servers...
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo.

REM Start Flask Main Server
echo Starting Flask Main Server (Port 3001)...
start "NeuroAid - Main Server [Port 3001]" cmd /k "cd flask_server && venv\Scripts\activate && python app.py"
timeout /t 2 >nul
echo ✅ Flask Main Server started
echo.

REM Start Chatbot Service
echo Starting Chatbot Service (Port 5001)...
start "NeuroAid - Chatbot [Port 5001]" cmd /k "cd ai_services\chatbot && venv\Scripts\activate && python app.py"
timeout /t 2 >nul
echo ✅ Chatbot Service started
echo.

REM Start Stroke Assessment Service
echo Starting Stroke Assessment Service (Port 5002)...
start "NeuroAid - Stroke Assessment [Port 5002]" cmd /k "cd ai_services\stroke_assessment && venv\Scripts\activate && python app.py"
timeout /t 2 >nul
echo ✅ Stroke Assessment Service started
echo.

REM Start Stroke Image Analysis Service
echo Starting Stroke Image Analysis Service (Port 5003)...
start "NeuroAid - Stroke Image Analysis [Port 5003]" cmd /k "cd ai_services\stroke_image && venv\Scripts\activate && python app.py"
timeout /t 2 >nul
echo ✅ Stroke Image Analysis Service started
echo.

echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo.

REM ========================================
REM   Step 4: Wait for Servers to Initialize
REM ========================================

echo [4/5] Waiting for Servers to Initialize...
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo.
echo Please wait while all servers start up...
echo.

REM Progress bar
for /l %%i in (1,1,10) do (
    echo ▓
    timeout /t 1 >nul
)
echo.
echo ✅ Initialization complete
echo.

echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo.

REM ========================================
REM   Step 5: Health Check
REM ========================================

echo [5/5] Performing Health Checks...
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo.

REM Check if curl is available
where curl >nul 2>&1
if errorlevel 1 (
    echo ⚠️  curl not found, skipping automated health checks
    echo    You can manually check health endpoints in your browser
    goto :skip_health_check
)

echo Checking server health...
echo.

REM Check Main Server
echo [1/4] Main Server (http://localhost:3001/health)
curl -s http://localhost:3001/health >nul 2>&1
if errorlevel 1 (
    echo     ❌ Main Server - NOT RESPONDING
    set MAIN_SERVER_STATUS=❌
) else (
    echo     ✅ Main Server - ONLINE
    set MAIN_SERVER_STATUS=✅
)
echo.

REM Check Chatbot
echo [2/4] Chatbot Service (http://localhost:5001/health)
curl -s http://localhost:5001/health >nul 2>&1
if errorlevel 1 (
    echo     ❌ Chatbot Service - NOT RESPONDING
    set CHATBOT_STATUS=❌
) else (
    echo     ✅ Chatbot Service - ONLINE
    set CHATBOT_STATUS=✅
)
echo.

REM Check Stroke Assessment
echo [3/4] Stroke Assessment Service (http://localhost:5002/health)
curl -s http://localhost:5002/health >nul 2>&1
if errorlevel 1 (
    echo     ❌ Stroke Assessment Service - NOT RESPONDING
    set ASSESSMENT_STATUS=❌
) else (
    echo     ✅ Stroke Assessment Service - ONLINE
    set ASSESSMENT_STATUS=✅
)
echo.

REM Check Stroke Image Analysis
echo [4/4] Stroke Image Analysis Service (http://localhost:5003/health)
curl -s http://localhost:5003/health >nul 2>&1
if errorlevel 1 (
    echo     ❌ Stroke Image Analysis Service - NOT RESPONDING
    set IMAGE_STATUS=❌
) else (
    echo     ✅ Stroke Image Analysis Service - ONLINE
    set IMAGE_STATUS=✅
)
echo.

:skip_health_check

echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo.

REM ========================================
REM   System Status Dashboard
REM ========================================

echo System Status Dashboard
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo.
echo ╔════════════════════════════════════════════════════════════════╗
echo ║                    SERVER STATUS DASHBOARD                     ║
echo ╠════════════════════════════════════════════════════════════════╣
echo ║                                                                ║
echo ║  %MAIN_SERVER_STATUS% Main Server (Flask)                                      ║
echo ║     • URL: http://localhost:3001                               ║
echo ║     • Health: http://localhost:3001/health                     ║
echo ║     • Config: http://localhost:3001/config                     ║
echo ║                                                                ║
echo ║  %CHATBOT_STATUS% Chatbot Service                                          ║
echo ║     • URL: http://localhost:5001                               ║
echo ║     • Health: http://localhost:5001/health                     ║
echo ║     • Endpoint: POST http://localhost:5001/chat                ║
echo ║                                                                ║
echo ║  %ASSESSMENT_STATUS% Stroke Assessment Service                                 ║
echo ║     • URL: http://localhost:5002                               ║
echo ║     • Health: http://localhost:5002/health                     ║
echo ║     • Endpoint: POST http://localhost:5002/predict             ║
echo ║                                                                ║
echo ║  %IMAGE_STATUS% Stroke Image Analysis Service                              ║
echo ║     • URL: http://localhost:5003                               ║
echo ║     • Health: http://localhost:5003/health                     ║
echo ║     • Endpoint: POST http://localhost:5003/analyze             ║
echo ║                                                                ║
echo ╚════════════════════════════════════════════════════════════════╝
echo.
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo.

REM ========================================
REM   Available API Endpoints
REM ========================================

echo ╔════════════════════════════════════════════════════════════════╗
echo ║                   AVAILABLE API ENDPOINTS                      ║
echo ╠════════════════════════════════════════════════════════════════╣
echo ║                                                                ║
echo ║  Authentication:                                               ║
echo ║    POST   /api/auth/register      - Register new user          ║
echo ║    POST   /api/auth/login         - Login user                 ║
echo ║                                                                ║
echo ║  AI Services:                                                  ║
echo ║    POST   /api/ai/chat            - AI Chatbot                 ║
echo ║    POST   /api/ai/stroke-assessment - Stroke Risk Assessment   ║
echo ║    POST   /api/ai/scan-image      - Scan Image Analysis        ║
echo ║                                                                ║
echo ║  User Management:                                              ║
echo ║    GET    /api/users              - Get all users              ║
echo ║    GET    /api/users/me           - Get current user           ║
echo ║                                                                ║
echo ║  Scans:                                                        ║
echo ║    GET    /api/scans              - Get user scans             ║
echo ║    POST   /api/scans              - Upload new scan            ║
echo ║    DELETE /api/scans/:id          - Delete scan                ║
echo ║                                                                ║
echo ║  Doctors:                                                      ║
echo ║    GET    /api/doctors            - Get all doctors            ║
echo ║    GET    /api/doctors/:id        - Get doctor by ID           ║
echo ║    POST   /api/doctors            - Create new doctor          ║
echo ║    PUT    /api/doctors/:id        - Update doctor              ║
echo ║    DELETE /api/doctors/:id        - Delete doctor              ║
echo ║                                                                ║
echo ║  Bookings:                                                     ║
echo ║    GET    /api/bookings           - Get user bookings          ║
echo ║    POST   /api/bookings           - Create booking             ║
echo ║    PUT    /api/bookings/:id       - Update booking             ║
echo ║    DELETE /api/bookings/:id       - Delete booking             ║
echo ║                                                                ║
echo ║  FAQs:                                                         ║
echo ║    GET    /api/faqs               - Get all FAQs               ║
echo ║    GET    /api/faqs/:id           - Get FAQ by ID              ║
echo ║                                                                ║
echo ║  Favorites:                                                    ║
echo ║    GET    /api/favorites          - Get user favorites         ║
echo ║    POST   /api/favorites          - Add to favorites           ║
echo ║    DELETE /api/favorites/:id      - Remove from favorites      ║
echo ║                                                                ║
echo ╚════════════════════════════════════════════════════════════════╝
echo.

echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo.

REM ========================================
REM   User Options
REM ========================================

echo ╔════════════════════════════════════════════════════════════════╗
echo ║                         OPTIONS MENU                           ║
echo ╠════════════════════════════════════════════════════════════════╣
echo ║                                                                ║
echo ║  [1] Open Health Checks in Browser                             ║
echo ║  [2] View API Documentation                                    ║
echo ║  [3] Keep Running (Minimize this window)                       ║
echo ║  [4] Exit (Stop all servers)                                   ║
echo ║                                                                ║
echo ╚════════════════════════════════════════════════════════════════╝
echo.

set /p choice="Enter your choice (1-4): "

if "%choice%"=="1" goto :open_health_checks
if "%choice%"=="2" goto :view_docs
if "%choice%"=="3" goto :keep_running
if "%choice%"=="4" goto :exit_servers
goto :invalid_choice

:open_health_checks
echo.
echo Opening health check pages in browser...
start http://localhost:3001/health
timeout /t 1 >nul
start http://localhost:5001/health
timeout /t 1 >nul
start http://localhost:5002/health
timeout /t 1 >nul
start http://localhost:5003/health
echo.
echo ✅ Health check pages opened
echo.
goto :keep_running

:view_docs
echo.
echo Opening API Documentation...
if exist "API_DOCUMENTATION.md" (
    start API_DOCUMENTATION.md
    echo ✅ API Documentation opened
) else (
    echo ⚠️  API_DOCUMENTATION.md not found
)
echo.
goto :keep_running

:keep_running
echo.
echo ╔════════════════════════════════════════════════════════════════╗
echo ║                   ALL SERVERS ARE RUNNING                      ║
echo ╠════════════════════════════════════════════════════════════════╣
echo ║                                                                ║
echo ║  All servers are running in separate windows.                  ║
echo ║  You can minimize this window and continue working.            ║
echo ║                                                                ║
echo ║  To stop all servers:                                          ║
echo ║  • Close all server windows manually, OR                       ║
echo ║  • Press any key in this window to stop all servers            ║
echo ║                                                                ║
echo ╚════════════════════════════════════════════════════════════════╝
echo.
pause
goto :exit_servers

:invalid_choice
echo.
echo ❌ Invalid choice. Please try again.
echo.
timeout /t 2 >nul
goto :keep_running

:exit_servers
echo.
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo.
echo Stopping all servers...
echo.
echo ⚠️  Please close all server windows manually.
echo    Look for windows titled:
echo    • NeuroAid - Main Server [Port 3001]
echo    • NeuroAid - Chatbot [Port 5001]
echo    • NeuroAid - Stroke Assessment [Port 5002]
echo    • NeuroAid - Stroke Image Analysis [Port 5003]
echo.
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo.
echo Thank you for using NeuroAid! 🚀
echo.
pause
exit
