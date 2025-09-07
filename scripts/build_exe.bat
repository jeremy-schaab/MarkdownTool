@echo off
REM Windows batch script to build executable
REM This is a wrapper around the Python build script

echo ========================================
echo  Markdown Manager - Executable Builder
echo ========================================
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ and try again
    pause
    exit /b 1
)

REM Run the Python build script
echo Building executable...
python scripts\build_exe.py

echo.
echo Build process completed.
echo Check the messages above for success/failure status.
echo.
pause