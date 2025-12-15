@echo off
echo Installing dependencies for all AI services...
echo.

echo [1/3] Installing Chatbot dependencies...
cd chatbot
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install chatbot dependencies
    pause
    exit /b 1
)
cd ..

echo.
echo [2/3] Installing Stroke Assessment dependencies...
cd stroke_assessment
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install stroke assessment dependencies
    pause
    exit /b 1
)
cd ..

echo.
echo [3/3] Installing Stroke Image Analysis dependencies...
cd stroke_image
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install stroke image dependencies
    pause
    exit /b 1
)
cd ..

echo.
echo ========================================
echo All dependencies installed successfully!
echo ========================================
echo.
echo You can now run: start_all_services.bat
echo.
pause
