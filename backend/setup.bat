@echo off
echo ========================================
echo Backend API - Setup Script
echo ========================================
echo.

echo [1/4] Creating virtual environment...
python -m venv venv
if errorlevel 1 (
    echo ERROR: Failed to create virtual environment
    echo Make sure Python 3.8+ is installed
    pause
    exit /b 1
)

echo [2/4] Activating virtual environment...
call venv\Scripts\activate.bat

echo [3/4] Installing dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)

echo [4/4] Creating .env file...
if not exist .env (
    copy .env.example .env
    echo .env file created! Please edit it and add your API keys.
) else (
    echo .env file already exists, skipping...
)

echo.
echo ========================================
echo Setup complete!
echo ========================================
echo.
echo Next steps:
echo 1. Edit .env file and add your API keys:
echo    - GROQ_API_KEY (get from https://console.groq.com)
echo    - COHERE_API_KEY (get from https://dashboard.cohere.com)
echo.
echo 2. Run the server:
echo    python main.py
echo.
pause
