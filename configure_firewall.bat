@echo off
REM ============================================
REM NeuroAid LAN Access - Firewall Configuration
REM ============================================
REM This script configures Windows Firewall to allow
REM incoming connections to the backend services
REM
REM MUST BE RUN AS ADMINISTRATOR
REM ============================================

echo.
echo ============================================
echo NeuroAid Firewall Configuration
echo ============================================
echo.

REM Check for administrator privileges
net session >nul 2>&1
if %errorLevel% NEQ 0 (
    echo [ERROR] This script requires Administrator privileges!
    echo.
    echo Please right-click this file and select "Run as Administrator"
    echo.
    pause
    exit /b 1
)

echo [INFO] Administrator privileges confirmed
echo.

REM Define ports
set GATEWAY_PORT=8080
set FLASK_PORT=5000
set CHATBOT_PORT=5001
set ASSESSMENT_PORT=5002
set IMAGE_PORT=5003

echo [INFO] Configuring firewall rules for the following ports:
echo   - Gateway: %GATEWAY_PORT%
echo   - Flask Server: %FLASK_PORT%
echo   - AI Chatbot: %CHATBOT_PORT%
echo   - Stroke Assessment: %ASSESSMENT_PORT%
echo   - Image Analysis: %IMAGE_PORT%
echo.

REM Remove existing rules (if any)
echo [INFO] Removing existing rules (if any)...
netsh advfirewall firewall delete rule name="NeuroAid Gateway" >nul 2>&1
netsh advfirewall firewall delete rule name="NeuroAid Flask Server" >nul 2>&1
netsh advfirewall firewall delete rule name="NeuroAid AI Chatbot" >nul 2>&1
netsh advfirewall firewall delete rule name="NeuroAid Stroke Assessment" >nul 2>&1
netsh advfirewall firewall delete rule name="NeuroAid Image Analysis" >nul 2>&1
echo [OK] Old rules removed
echo.

REM Add new firewall rules
echo [INFO] Adding new firewall rules...

REM Gateway (Port 8080)
netsh advfirewall firewall add rule name="NeuroAid Gateway" dir=in action=allow protocol=TCP localport=%GATEWAY_PORT% profile=private
if %errorLevel% EQU 0 (
    echo [OK] Gateway port %GATEWAY_PORT% configured
) else (
    echo [ERROR] Failed to configure Gateway port
)

REM Flask Server (Port 5000)
netsh advfirewall firewall add rule name="NeuroAid Flask Server" dir=in action=allow protocol=TCP localport=%FLASK_PORT% profile=private
if %errorLevel% EQU 0 (
    echo [OK] Flask Server port %FLASK_PORT% configured
) else (
    echo [ERROR] Failed to configure Flask Server port
)

REM AI Chatbot (Port 5001)
netsh advfirewall firewall add rule name="NeuroAid AI Chatbot" dir=in action=allow protocol=TCP localport=%CHATBOT_PORT% profile=private
if %errorLevel% EQU 0 (
    echo [OK] AI Chatbot port %CHATBOT_PORT% configured
) else (
    echo [ERROR] Failed to configure AI Chatbot port
)

REM Stroke Assessment (Port 5002)
netsh advfirewall firewall add rule name="NeuroAid Stroke Assessment" dir=in action=allow protocol=TCP localport=%ASSESSMENT_PORT% profile=private
if %errorLevel% EQU 0 (
    echo [OK] Stroke Assessment port %ASSESSMENT_PORT% configured
) else (
    echo [ERROR] Failed to configure Stroke Assessment port
)

REM Image Analysis (Port 5003)
netsh advfirewall firewall add rule name="NeuroAid Image Analysis" dir=in action=allow protocol=TCP localport=%IMAGE_PORT% profile=private
if %errorLevel% EQU 0 (
    echo [OK] Image Analysis port %IMAGE_PORT% configured
) else (
    echo [ERROR] Failed to configure Image Analysis port
)

echo.
echo ============================================
echo Firewall Configuration Complete!
echo ============================================
echo.
echo All required ports are now allowed through the firewall.
echo.
echo IMPORTANT NOTES:
echo 1. These rules only apply to "Private" networks (home/work)
echo 2. Make sure your WiFi is set to "Private Network" mode
echo 3. To verify, run: netsh advfirewall firewall show rule name=all
echo.
echo Next Steps:
echo 1. Start the backend: run start_system.bat
echo 2. Note the LAN IP address shown in the terminal
echo 3. Update that IP in your Flutter app's api_constants.dart
echo 4. Test from your mobile device
echo.
pause
