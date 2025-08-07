#!/bin/bash

# Cursor IDE Demo - macOS Launch Script
# This script launches the cross-platform Pygame demo application

echo ""
echo "========================================"
echo "   Cursor IDE Demo - macOS Launcher"
echo "========================================"
echo ""

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check if Python is installed
if ! command_exists python3; then
    echo "ERROR: Python 3 is not installed or not in PATH"
    echo "Please install Python 3.8+ using one of these methods:"
    echo "  1. Download from https://python.org"
    echo "  2. Using Homebrew: brew install python"
    echo "  3. Using pyenv: pyenv install 3.12.8"
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
    
    # Try different pip commands
    if command_exists pip3; then
        pip3 install -r requirements.txt
    elif command_exists pip; then
        pip install -r requirements.txt
    else
        python3 -m pip install -r requirements.txt
    fi
    
    if [ $? -ne 0 ]; then
        echo "ERROR: Failed to install dependencies"
        echo "Try installing system dependencies first:"
        echo "  brew install pkg-config sdl2 sdl2_image sdl2_mixer sdl2_ttf"
        echo "  brew install portmidi"
        exit 1
    fi
fi

# Create logs directory if it doesn't exist
mkdir -p logs

# Check for display server (macOS should always have one)
if [ -z "$DISPLAY" ] && [ "$(uname)" = "Darwin" ]; then
    # On macOS, we don't need DISPLAY variable
    echo "macOS detected - display server should be available"
fi

# Check if running on Apple Silicon
if [ "$(uname -m)" = "arm64" ]; then
    echo "Apple Silicon (M1/M2/M3) detected - using optimized settings"
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
    echo ""
    echo "Common macOS issues and solutions:"
    echo "  1. If pygame fails to initialize: brew install sdl2 sdl2_image sdl2_mixer sdl2_ttf"
    echo "  2. If audio fails: brew install portmidi"
    echo "  3. If permissions denied: chmod +x launch_mac.sh"
    exit 1
fi

echo ""
echo "Demo completed successfully!" 