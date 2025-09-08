@echo off
REM Windows batch script to build professional installer
REM This creates both the executable and the installer

echo ===============================================================
echo  Markdown Manager - Professional Installer Builder
echo ===============================================================
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ and try again
    pause
    exit /b 1
)

REM Check if we're in the right directory
if not exist "scripts\build_installer.py" (
    echo ERROR: build_installer.py not found
    echo Please run this script from the project root directory
    pause
    exit /b 1
)

echo This script will:
echo 1. Create application icon
echo 2. Build Windows executable
echo 3. Create professional installer with Inno Setup
echo 4. Package everything for distribution
echo.

REM Check if Inno Setup is installed
set INNO_PATH_1="C:\Program Files (x86)\Inno Setup 6\ISCC.exe"
set INNO_PATH_2="C:\Program Files\Inno Setup 6\ISCC.exe"

if exist %INNO_PATH_1% goto :inno_found
if exist %INNO_PATH_2% goto :inno_found

echo WARNING: Inno Setup not detected
echo To create professional installer, please install Inno Setup 6:
echo https://jrsoftware.org/isdl.php
echo.
echo The script will still create a standalone executable.
echo.

:inno_found
echo Starting build process...
echo.

REM Run the Python build script
python scripts\build_installer.py

echo.
echo Build process completed.
echo Check the messages above for success/failure status.
echo.

REM Show results
echo Results Summary:
echo ---------------
if exist "installer\output\*.exe" (
    echo [SUCCESS] Professional installer created
    dir "installer\output\*.exe" /b
)
if exist "release\MarkdownManager-Standalone.exe" (
    echo [SUCCESS] Standalone executable created
)
if exist "MarkdownManager-v1.2.0-Complete.zip" (
    echo [SUCCESS] Complete distribution package created
)

echo.
echo Files ready for distribution!
echo.
pause