#!/bin/bash

# A-Player Hiring Suite Launch Script
# This script starts the application in production mode

echo "=================================================="
echo "  A-Player Hiring Suite"
echo "  Evidence-Based Hiring & Leadership Assessment"
echo "=================================================="
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.11 or later."
    exit 1
fi

# Check if we're in the correct directory
if [ ! -d "backend" ]; then
    echo "❌ Error: Please run this script from the A_Player_Hiring_Suite directory"
    exit 1
fi

cd backend

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
    echo "✓ Virtual environment created"
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Check if dependencies are installed
if [ ! -f "venv/installed.marker" ]; then
    echo "📦 Installing dependencies..."
    pip install -r requirements.txt
    touch venv/installed.marker
    echo "✓ Dependencies installed"
fi

# Check if static files exist (frontend build)
if [ ! -d "static/assets" ]; then
    echo "⚠️  Warning: Frontend build not found in backend/static/"
    echo "   To build the frontend:"
    echo "   1. cd frontend"
    echo "   2. npm install"
    echo "   3. npm run build"
    echo "   4. cp -r dist ../backend/static"
    echo ""
    echo "   Running backend only (API will be available at http://localhost:8000/api/docs)"
fi

# Start the server
echo ""
echo "🚀 Starting A-Player Hiring Suite..."
echo "📍 Access at: http://localhost:8000"
echo "📚 API docs: http://localhost:8000/api/docs"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

python run.py
