#!/bin/bash

echo "🚀 Setting up Secure Expense Tracker - Full Stack Edition"
echo "========================================================"
echo "Python CLI + Spring Boot REST API + Comprehensive Security"
echo ""

# Check prerequisites
echo "Checking prerequisites..."

# Check Python
if command -v python3 &> /dev/null; then
    echo "✅ Python 3 found: $(python3 --version)"
else
    echo "❌ Python 3 not found. Please install Python 3.8+"
    exit 1
fi

# Check Java
if command -v java &> /dev/null; then
    echo "✅ Java found: $(java -version 2>&1 | head -n 1)"
else
    echo "❌ Java not found. Please install Java 17+"
    exit 1
fi

# Check Maven
if command -v mvn &> /dev/null; then
    echo "✅ Maven found: $(mvn -version | head -n 1)"
else
    echo "❌ Maven not found. Please install Maven 3.6+"
    exit 1
fi

echo ""
echo "🐍 Setting up Python CLI Application..."
echo "----------------------------------------"

# Setup Python virtual environment
python3 -m venv venv
source venv/bin/activate

# Install Python dependencies
echo "Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Initialize Python database
echo "Initializing Python CLI database..."
python tracker.py init

echo "✅ Python CLI setup complete!"

echo ""
echo "☕ Setting up Spring Boot API..."
echo "--------------------------------"

# Navigate to backend directory
cd backend-api

# Build Spring Boot application
echo "Building Spring Boot application..."
mvn clean compile

# Run tests
echo "Running Spring Boot tests..."
mvn test

echo "✅ Spring Boot API setup complete!"

cd ..

echo ""
echo "🎉 Setup completed successfully!"
echo ""
echo "📋 Available Applications:"
echo ""
echo "1. 🐍 Python CLI Application:"
echo "   • Command: source venv/bin/activate && python tracker.py start"
echo "   • Features: Interactive CLI, local SQLite, AES encryption"
echo "   • Perfect for: Personal use, terminal-based expense tracking"
echo ""
echo "2. ☕ Spring Boot REST API:"
echo "   • Command: cd backend-api && mvn spring-boot:run"
echo "   • URL: http://localhost:8080"
echo "   • Swagger UI: http://localhost:8080/swagger-ui.html"
echo "   • Features: RESTful API, JWT auth, H2/PostgreSQL, comprehensive analytics"
echo "   • Perfect for: Web apps, mobile apps, enterprise integration"
echo ""
echo "🔗 Integration Options:"
echo "   • Both apps can share the same database"
echo "   • Python CLI can call Spring Boot API endpoints"
echo "   • Use Spring Boot for web/mobile, Python CLI for admin tasks"
echo ""
echo "🔐 Security Features (Both Apps):"
echo "   ✅ AES-256 encryption for sensitive data"
echo "   ✅ Secure password hashing (bcrypt)"
echo "   ✅ Account lockout protection"
echo "   ✅ Input validation and sanitization"
echo "   ✅ JWT authentication (Spring Boot)"
echo ""
echo "📊 Analytics & Reports:"
echo "   ✅ Monthly spending reports with ASCII charts"
echo "   ✅ Category-wise breakdowns"
echo "   ✅ Spending trends and statistics"
echo "   ✅ Export to CSV/PDF"
echo ""
echo "🧪 Testing:"
echo "   • Python: python -m pytest test_tracker.py -v"
echo "   • Spring Boot: cd backend-api && mvn test"
echo ""
echo "Ready to track expenses securely! 💰🔒"
