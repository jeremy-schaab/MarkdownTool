@echo off
REM Markdown Manager Windows Installer
REM Simple batch file for quick installation

echo === Markdown Manager Installer ===
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://www.python.org/downloads/
    echo Make sure to check "Add Python to PATH" during installation
    pause
    exit /b 1
)

echo Python found!
python --version

REM Install dependencies
echo.
echo Installing Python dependencies...
python -m pip install --upgrade pip
python -m pip install streamlit markdown pygments streamlit-ace openai python-dotenv

if %errorlevel% neq 0 (
    echo Error: Failed to install dependencies
    pause
    exit /b 1
)

echo.
echo Dependencies installed successfully!

REM Check if .env file exists
if not exist ".env" (
    if exist ".env.example" (
        echo Creating .env configuration file...
        copy ".env.example" ".env"
        echo.
        echo IMPORTANT: Please edit .env file with your Azure OpenAI credentials
        echo File location: %cd%\.env
        echo.
    )
)

echo.
echo ==========================================
echo  Markdown Manager installed successfully!
echo ==========================================
echo.
echo To run the application:
echo   1. Configure your Azure OpenAI credentials in .env file
echo   2. Double-click run_app.bat
echo   3. Or run: python run_app.py
echo.
echo Press any key to start the application now...
pause >nul

python run_app.py