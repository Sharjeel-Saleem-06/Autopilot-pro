#!/bin/bash
# Autopilot Pro Launcher Script for Unix/Linux/macOS
# ===================================================

echo "🚗 Starting Autopilot Pro..."
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null && ! command -v python &> /dev/null; then
    echo "❌ Python is not installed. Please install Python 3.8 or higher."
    exit 1
fi

# Determine Python command
if command -v python3 &> /dev/null; then
    PYTHON_CMD=python3
else
    PYTHON_CMD=python
fi

# Check if requirements are installed
echo "📦 Checking dependencies..."
$PYTHON_CMD -c "import gradio, ultralytics, cv2" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "⚠️  Some dependencies are missing."
    echo "📥 Installing requirements..."
    $PYTHON_CMD -m pip install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo "❌ Failed to install dependencies."
        exit 1
    fi
fi

# Launch the main script
echo "🚀 Launching all models..."
echo ""
$PYTHON_CMD launch_all.py

