@echo off
REM Time Series AI Forecasting Platform - Setup Script for Windows

echo ============================================
echo Time Series AI Platform Setup
echo ============================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://www.python.org/downloads/
    pause
    exit /b 1
)

echo [1/5] Creating Python virtual environment...
python -m venv venv
call venv\Scripts\activate.bat

echo [2/5] Upgrading pip...
python -m pip install --upgrade pip

echo [3/5] Installing required packages...
pip install -r requirements.txt

echo [4/5] Creating necessary directories...
mkdir data 2>nul
mkdir models 2>nul
mkdir logs 2>nul

echo [5/5] Setup completed successfully!
echo.
echo To activate the virtual environment, run:
echo   venv\Scripts\activate.bat
echo.
echo To start the Flask server, run:
echo   python run.py
echo.
echo Then open http://localhost:5000 in your browser
echo.
pause
