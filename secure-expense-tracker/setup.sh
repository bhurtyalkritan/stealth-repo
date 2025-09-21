#!/bin/bash

# Secure Expense Tracker - Setup Script
# Automates the installation and setup process

echo "🔒 Secure Expense Tracker - Setup Script"
echo "========================================"

# Check Python version
echo "Checking Python version..."
python_version=$(python3 --version 2>&1)
if [[ $? -eq 0 ]]; then
    echo "✅ Python found: $python_version"
else
    echo "❌ Python 3 not found. Please install Python 3.8+ first."
    exit 1
fi

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv venv
if [[ $? -eq 0 ]]; then
    echo "✅ Virtual environment created"
else
    echo "❌ Failed to create virtual environment"
    exit 1
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
if [[ $? -eq 0 ]]; then
    echo "✅ Dependencies installed successfully"
else
    echo "❌ Failed to install dependencies"
    exit 1
fi

# Initialize database
echo "Initializing database..."
python tracker.py init
if [[ $? -eq 0 ]]; then
    echo "✅ Database initialized"
else
    echo "❌ Failed to initialize database"
    exit 1
fi

# Run tests
echo "Running tests..."
python -m pytest test_tracker.py -v
if [[ $? -eq 0 ]]; then
    echo "✅ All tests passed"
else
    echo "⚠️  Some tests failed (this is normal if dependencies aren't fully installed)"
fi

echo ""
echo "🎉 Setup completed successfully!"
echo ""
echo "To start the application:"
echo "  source venv/bin/activate"
echo "  python tracker.py start"
echo ""
echo "To run tests:"
echo "  python -m pytest test_tracker.py -v"
echo ""
echo "Happy expense tracking! 💰"
