@echo off
REM Cursor IDE Demo - Windows Launch Script
REM This script launches the cross-platform Pygame demo application

echo.
echo ========================================
echo    Cursor IDE Demo - Windows Launcher
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://python.org
    pause
    exit /b 1
)

echo Python found: 
python --version

REM Check if we're in the correct directory
if not exist "app\main.py" (
    echo ERROR: app\main.py not found
    echo Please run this script from the CursorDemo directory
    pause
    exit /b 1
)

REM Check if requirements are installed
echo.
echo Checking dependencies...
python -c "import pygame, psutil, numpy, PIL" >nul 2>&1
if errorlevel 1 (
    echo Installing required packages...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo ERROR: Failed to install dependencies
        pause
        exit /b 1
    )
)

REM Create logs directory if it doesn't exist
if not exist "logs" mkdir logs

echo.
echo Starting Cursor IDE Demo...
echo Press Ctrl+C to exit
echo.

REM Launch the application with error handling and disabled failsafe
set CURSOR_DEMO_DISABLE_FAILSAFE=true
python app/main.py

REM Check exit code
if errorlevel 1 (
    echo.
    echo ERROR: Application crashed or encountered an error
    echo Check the logs directory for detailed error information
    pause
    exit /b 1
)

echo.
echo Demo completed successfully!
pause 