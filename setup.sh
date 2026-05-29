#!/bin/bash
# Time Series AI Forecasting Platform - Setup Script for Linux/Mac

echo "============================================"
echo "Time Series AI Platform Setup"
echo "============================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed"
    echo "Please install Python 3.8+ from https://www.python.org/downloads/"
    exit 1
fi

echo "[1/5] Creating Python virtual environment..."
python3 -m venv venv
source venv/bin/activate

echo "[2/5] Upgrading pip..."
python3 -m pip install --upgrade pip

echo "[3/5] Installing required packages..."
pip install -r requirements.txt

echo "[4/5] Creating necessary directories..."
mkdir -p data models logs

echo "[5/5] Setup completed successfully!"
echo ""
echo "To activate the virtual environment, run:"
echo "  source venv/bin/activate"
echo ""
echo "To start the Flask server, run:"
echo "  python run.py"
echo ""
echo "Then open http://localhost:5000 in your browser"
echo ""
