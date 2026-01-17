#!/bin/bash
# Installation script for Campus Connect AI Engine

echo "========================================"
echo "Campus Connect AI Engine - Installation"
echo "========================================"

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

echo "Python version:"
python3 --version

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Create uploads directory
if [ ! -d "uploads" ]; then
    echo "Creating uploads directory..."
    mkdir uploads
fi

echo ""
echo "========================================"
echo "Installation completed successfully!"
echo "========================================"
echo ""
echo "To start the server, run:"
echo "  python start_server.py"
echo "  or"
echo "  python main.py"
echo ""
echo "Then visit http://localhost:8000/docs for API documentation"
echo ""


