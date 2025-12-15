@echo off
REM ============================================
REM NeuroAid LAN Backend Startup Script
REM ============================================
REM This script starts the API Gateway for LAN access
REM and displays all necessary configuration information
REM ============================================

title NeuroAid LAN Backend

echo.
echo ============================================================
echo                  NeuroAid LAN Backend Startup
echo ============================================================
echo.

REM Get local IP address
for /f "tokens=2 delims=:" %%a in ('ipconfig ^| findstr /c:"IPv4 Address"') do (
    set IP=%%a
    goto :found_ip
)
:found_ip
set IP=%IP:~1%

echo [INFO] Detecting network configuration...
echo.
echo ============================================================
echo                    Network Information
echo ============================================================
echo.
echo Local IP Address: %IP%
echo Gateway Port: 8080
echo.
echo IMPORTANT: Make sure you are connected to WiFi!
echo.

REM Check if firewall is configured
echo [INFO] Checking firewall configuration...
netsh advfirewall firewall show rule name="NeuroAid Gateway" >nul 2>&1
if %errorLevel% NEQ 0 (
    echo.
    echo ============================================================
    echo                  WARNING: Firewall Not Configured!
    echo ============================================================
    echo.
    echo The Windows Firewall is not configured for LAN access.
    echo.
    echo Please run: configure_firewall.bat (as Administrator)
    echo.
    echo Press any key to continue anyway, or Ctrl+C to exit...
    pause >nul
    echo.
) else (
    echo [OK] Firewall rules configured
    echo.
)

REM Display configuration for Flutter app
echo ============================================================
echo            Configuration for Flutter App
echo ============================================================
echo.
echo File: lib\src\core\constants\api_constants.dart
echo.
echo Update this line:
echo   static const String _networkIp = '%IP%';
echo.

REM Display testing URLs
echo ============================================================
echo                  Testing URLs
echo ============================================================
echo.
echo Test from mobile browser:
echo   http://%IP%:8080/health
echo.
echo Expected response:
echo   {"gateway": "OK", "services": {...}}
echo.

REM Display connection checklist
echo ============================================================
echo              Pre-Launch Checklist
echo ============================================================
echo.
echo [ ] Backend firewall configured (configure_firewall.bat)
echo [ ] Laptop connected to WiFi
echo [ ] Mobile device on SAME WiFi network
echo [ ] Flutter app updated with IP: %IP%
echo [ ] All required ports available (8080, 5000, 5001, 5002)
echo.

echo ============================================================
echo              Starting API Gateway...
echo ============================================================
echo.
echo Gateway will be accessible at:
echo   - LAN:  http://%IP%:8080
echo   - Local: http://localhost:8080
echo.
echo Press Ctrl+C to stop the server
echo.
echo ============================================================
echo.

REM Set environment variable for gateway port
set GATEWAY_PORT=8080

REM Start the gateway
echo [INFO] Launching API Gateway...
echo.
python gateway.py

REM If Python exits
echo.
echo ============================================================
echo Gateway Stopped
echo ============================================================
echo.
pause
