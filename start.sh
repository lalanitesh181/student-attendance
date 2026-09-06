#!/bin/bash
# Deployment helper script

echo "Smart Attendance App - Deployment Helper"
echo "========================================"
echo ""

# Check Python
if command -v python3 &> /dev/null; then
    echo "Python3 is installed"
    python3 --version
else
    echo "ERROR: Python3 is not installed!"
    exit 1
fi

# Check pip
if command -v pip3 &> /dev/null; then
    echo "pip3 is installed"
else
    echo "ERROR: pip3 is not installed!"
    exit 1
fi

# Install dependencies
echo ""
echo "Installing dependencies..."
pip3 install -r requirements.txt

# Check if Firebase credentials exist
if [ -f "firebase_service_account.json" ]; then
    echo ""
    echo "Firebase credentials found!"
else
    echo ""
    echo "WARNING: firebase_service_account.json not found!"
    echo "The app will run in DEMO mode (data will be lost on restart)."
    echo "To connect Firebase:"
    echo "  1. Go to https://console.firebase.google.com/"
    echo "  2. Create a project and download serviceAccountKey.json"
    echo "  3. Rename it to firebase_service_account.json and place here"
fi

echo ""
echo "Starting the application..."
echo "Open http://localhost:5000 in your browser"
echo ""
python3 app.py
