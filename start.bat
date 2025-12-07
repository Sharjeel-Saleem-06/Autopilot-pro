@echo off
REM Autopilot Pro Launcher Script for Windows
REM ==========================================

echo.
echo 🚗 Starting Autopilot Pro...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed. Please install Python 3.8 or higher.
    pause
    exit /b 1
)

REM Check if requirements are installed
echo 📦 Checking dependencies...
python -c "import gradio, ultralytics, cv2" >nul 2>&1
if errorlevel 1 (
    echo ⚠️  Some dependencies are missing.
    echo 📥 Installing requirements...
    python -m pip install -r requirements.txt
    if errorlevel 1 (
        echo ❌ Failed to install dependencies.
        pause
        exit /b 1
    )
)

REM Launch the main script
echo 🚀 Launching all models...
echo.
python launch_all.py

pause

