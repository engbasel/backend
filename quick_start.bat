@echo off
echo.
echo ╔════════════════════════════════════════════════════════════════╗
echo ║            Quick Start - NeuroAid Backend                      ║
echo ╚════════════════════════════════════════════════════════════════╝
echo.
echo Starting all servers...
echo.

start "NeuroAid - Main Server" cmd /k "cd flask_server && venv\Scripts\activate && python app.py"
timeout /t 3 >nul

start "NeuroAid - Chatbot" cmd /k "cd ai_services\chatbot && venv\Scripts\activate && python app.py"
timeout /t 2 >nul

start "NeuroAid - Stroke Assessment" cmd /k "cd ai_services\stroke_assessment && venv\Scripts\activate && python app.py"
timeout /t 2 >nul

start "NeuroAid - Stroke Image" cmd /k "cd ai_services\stroke_image && venv\Scripts\activate && python app.py"

echo.
echo ✅ All servers started!
echo.
echo Main Server: http://localhost:3001
echo Chatbot: http://localhost:5001
echo Stroke Assessment: http://localhost:5002
echo Image Analysis: http://localhost:5003
echo.
echo Press any key to exit...
pause >nul
