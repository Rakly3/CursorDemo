#!/bin/bash

# Cursor IDE Demo - Linux Launch Script
# This script launches the cross-platform Pygame demo application

echo ""
echo "========================================"
echo "   Cursor IDE Demo - Linux Launcher"
echo "========================================"
echo ""

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check if Python is installed
if ! command_exists python3; then
    echo "ERROR: Python 3 is not installed or not in PATH"
    echo "Please install Python 3.8+ using your package manager:"
    echo "  Ubuntu/Debian: sudo apt install python3 python3-pip"
    echo "  Fedora: sudo dnf install python3 python3-pip"
    echo "  Arch: sudo pacman -S python python-pip"
    exit 1
fi

echo "Python found:"
python3 --version

# Check if we're in the correct directory
if [ ! -f "app/main.py" ]; then
    echo "ERROR: app/main.py not found"
    echo "Please run this script from the CursorDemo directory"
    exit 1
fi

# Check if requirements are installed
echo ""
echo "Checking dependencies..."
if ! python3 -c "import pygame, psutil, numpy, PIL" 2>/dev/null; then
    echo "Installing required packages..."
    if command_exists pip3; then
        pip3 install -r requirements.txt
    else
        python3 -m pip install -r requirements.txt
    fi
    
    if [ $? -ne 0 ]; then
        echo "ERROR: Failed to install dependencies"
        echo "Try running: sudo apt install python3-dev python3-pip"
        exit 1
    fi
fi

# Create logs directory if it doesn't exist
mkdir -p logs

# Check for display server
if [ -z "$DISPLAY" ] && ! command_exists wsl.exe; then
    echo "WARNING: No display server detected"
    echo "If running on WSL, make sure you have an X server running"
    echo "If running on a headless server, the demo may not work properly"
fi

echo ""
echo "Starting Cursor IDE Demo..."
echo "Press Ctrl+C to exit"
echo ""

# Launch the application with error handling
python3 app/main.py

# Check exit code
if [ $? -ne 0 ]; then
    echo ""
    echo "ERROR: Application crashed or encountered an error"
    echo "Check the logs directory for detailed error information"
    exit 1
fi

echo ""
echo "Demo completed successfully!" 