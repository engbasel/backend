@echo off
setlocal enabledelayedexpansion
title NeuroAid - Endpoint Testing Tool
color 0E

echo.
echo ╔════════════════════════════════════════════════════════════════╗
echo ║              NeuroAid - Endpoint Testing Tool                  ║
echo ╚════════════════════════════════════════════════════════════════╝
echo.

REM Check if curl is available
where curl >nul 2>&1
if errorlevel 1 (
    echo ❌ ERROR: curl is not installed!
    echo.
    echo curl is required for testing endpoints.
    echo Please install curl or use Git Bash which includes curl.
    echo.
    pause
    exit /b 1
)

echo ✅ curl is available
echo.

echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo.
echo Testing All Endpoints...
echo.

REM ========================================
REM   Test Main Server
REM ========================================

echo ╔════════════════════════════════════════════════════════════════╗
echo ║                    MAIN SERVER (Port 3001)                     ║
echo ╚════════════════════════════════════════════════════════════════╝
echo.

echo [1] Testing Health Endpoint...
echo URL: GET http://localhost:3001/health
echo.
curl -s -w "Status Code: %%{http_code}\n" http://localhost:3001/health
echo.
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo.

echo [2] Testing Config Endpoint...
echo URL: GET http://localhost:3001/config
echo.
curl -s -w "Status Code: %%{http_code}\n" http://localhost:3001/config
echo.
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo.

REM ========================================
REM   Test Chatbot Service
REM ========================================

echo ╔════════════════════════════════════════════════════════════════╗
echo ║                  CHATBOT SERVICE (Port 5001)                   ║
echo ╚════════════════════════════════════════════════════════════════╝
echo.

echo [3] Testing Chatbot Health...
echo URL: GET http://localhost:5001/health
echo.
curl -s -w "Status Code: %%{http_code}\n" http://localhost:5001/health
echo.
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo.

echo [4] Testing Chatbot Endpoint...
echo URL: POST http://localhost:5001/chat
echo.
curl -s -X POST http://localhost:5001/chat ^
  -H "Content-Type: application/json" ^
  -d "{\"message\": \"مرحبا\"}" ^
  -w "\nStatus Code: %%{http_code}\n"
echo.
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo.

REM ========================================
REM   Test Stroke Assessment Service
REM ========================================

echo ╔════════════════════════════════════════════════════════════════╗
echo ║            STROKE ASSESSMENT SERVICE (Port 5002)               ║
echo ╚════════════════════════════════════════════════════════════════╝
echo.

echo [5] Testing Stroke Assessment Health...
echo URL: GET http://localhost:5002/health
echo.
curl -s -w "Status Code: %%{http_code}\n" http://localhost:5002/health
echo.
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo.

echo [6] Testing Stroke Assessment Prediction...
echo URL: POST http://localhost:5002/predict
echo.
curl -s -X POST http://localhost:5002/predict ^
  -H "Content-Type: application/json" ^
  -d "{\"age\": 65, \"gender\": \"Male\", \"hypertension\": 1, \"heart_disease\": 0, \"avg_glucose_level\": 120, \"bmi\": 28.5, \"smoking_status\": \"formerly smoked\"}" ^
  -w "\nStatus Code: %%{http_code}\n"
echo.
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo.

REM ========================================
REM   Test Stroke Image Analysis Service
REM ========================================

echo ╔════════════════════════════════════════════════════════════════╗
echo ║          STROKE IMAGE ANALYSIS SERVICE (Port 5003)             ║
echo ╚════════════════════════════════════════════════════════════════╝
echo.

echo [7] Testing Stroke Image Analysis Health...
echo URL: GET http://localhost:5003/health
echo.
curl -s -w "Status Code: %%{http_code}\n" http://localhost:5003/health
echo.
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo.

echo Note: Image analysis endpoint requires multipart/form-data with image file
echo       Use Postman or similar tool to test image upload
echo.

REM ========================================
REM   Test Main Server API Endpoints
REM ========================================

echo ╔════════════════════════════════════════════════════════════════╗
echo ║                  MAIN SERVER API ENDPOINTS                     ║
echo ╚════════════════════════════════════════════════════════════════╝
echo.

echo [8] Testing Doctors Endpoint (GET all)...
echo URL: GET http://localhost:3001/api/doctors
echo.
curl -s -w "Status Code: %%{http_code}\n" http://localhost:3001/api/doctors
echo.
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo.

echo [9] Testing Doctors Endpoint (GET by ID)...
echo URL: GET http://localhost:3001/api/doctors/1
echo.
curl -s -w "Status Code: %%{http_code}\n" http://localhost:3001/api/doctors/1
echo.
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo.

echo [10] Testing Doctors Endpoint (CREATE)...
echo URL: POST http://localhost:3001/api/doctors
echo.
curl -s -X POST http://localhost:3001/api/doctors ^
  -H "Content-Type: application/json" ^
  -d "{\"name\": \"Dr. Test Doctor\", \"specialty\": \"Testing\", \"experience\": \"5 years\", \"rating\": 4.5}" ^
  -w "\nStatus Code: %%{http_code}\n"
echo.
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo.

echo [11] Testing FAQs Endpoint...
echo URL: GET http://localhost:3001/api/faqs
echo.
curl -s -w "Status Code: %%{http_code}\n" http://localhost:3001/api/faqs
echo.
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo.

REM ========================================
REM   Summary
REM ========================================

echo ╔════════════════════════════════════════════════════════════════╗
echo ║                       TESTING COMPLETE                         ║
echo ╠════════════════════════════════════════════════════════════════╣
echo ║                                                                ║
echo ║  All endpoint tests have been completed.                       ║
echo ║                                                                ║
echo ║  Status Code 200 = Success ✅                                  ║
echo ║  Status Code 4xx/5xx = Error ❌                                ║
echo ║                                                                ║
echo ║  For detailed API testing, use:                                ║
echo ║  • Postman                                                     ║
echo ║  • Insomnia                                                    ║
echo ║  • Thunder Client (VS Code Extension)                          ║
echo ║                                                                ║
echo ╚════════════════════════════════════════════════════════════════╝
echo.

pause
