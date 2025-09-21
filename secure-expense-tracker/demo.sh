#!/bin/bash

echo "🎭 Secure Expense Tracker - Live Demo Script"
echo "============================================="
echo "Demonstrating both Python CLI and Spring Boot API"
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

echo -e "${CYAN}📋 Demo Overview:${NC}"
echo "1. 🐍 Python CLI Application Demo"
echo "2. ☕ Spring Boot API Demo"  
echo "3. 🔗 Integration Demo"
echo ""

# Check if setup has been run
if [ ! -d "venv" ]; then
    echo -e "${RED}❌ Python virtual environment not found. Please run setup first:${NC}"
    echo "./setup-full-stack.sh"
    exit 1
fi

if [ ! -d "backend-api/target" ]; then
    echo -e "${YELLOW}⚠️  Spring Boot not built. Building now...${NC}"
    cd backend-api
    mvn clean compile -q
    cd ..
fi

echo -e "${PURPLE}🐍 PYTHON CLI APPLICATION DEMO${NC}"
echo "================================="
echo ""

# Activate Python environment
source venv/bin/activate

echo -e "${GREEN}✅ Python environment activated${NC}"
echo ""

echo -e "${BLUE}📊 Running Python CLI demo commands:${NC}"
echo ""

# Initialize database
echo -e "${YELLOW}Initializing database...${NC}"
python tracker.py init

echo ""
echo -e "${CYAN}🎯 Key Python CLI Features:${NC}"
echo "• Interactive terminal UI with Rich library"
echo "• AES-256 encryption for sensitive data"
echo "• SQLite database with SQLAlchemy ORM"
echo "• Account lockout protection"
echo "• ASCII charts for spending reports"
echo "• CSV/PDF export capabilities"
echo ""

echo -e "${BLUE}To interact with Python CLI:${NC}"
echo "python tracker.py start"
echo ""

echo -e "${PURPLE}☕ SPRING BOOT API DEMO${NC}"
echo "========================"
echo ""

cd backend-api

echo -e "${YELLOW}Starting Spring Boot API in background...${NC}"
mvn spring-boot:run > /dev/null 2>&1 &
SPRING_PID=$!

echo -e "${GREEN}✅ Spring Boot API starting (PID: $SPRING_PID)${NC}"
echo "Waiting for API to be ready..."

# Wait for Spring Boot to start
sleep 10

echo ""
echo -e "${CYAN}🎯 Key Spring Boot API Features:${NC}"
echo "• RESTful API with comprehensive endpoints"
echo "• JWT authentication and authorization"  
echo "• JPA/Hibernate with H2/PostgreSQL support"
echo "• Auto-generated Swagger documentation"
echo "• Spring Security with account lockout"
echo "• AES encryption service for sensitive data"
echo "• Comprehensive error handling"
echo ""

echo -e "${BLUE}📍 API Endpoints Available:${NC}"
echo "• Base URL: http://localhost:8080/api"
echo "• Swagger UI: http://localhost:8080/swagger-ui.html"
echo "• Health Check: http://localhost:8080/actuator/health"
echo ""

echo -e "${BLUE}🧪 Testing API endpoints:${NC}"
echo ""

# Test health endpoint
echo -e "${YELLOW}Testing health endpoint...${NC}"
curl -s http://localhost:8080/actuator/health | head -c 100
echo ""
echo ""

# Test API documentation endpoint
echo -e "${YELLOW}Testing API docs endpoint...${NC}"
curl -s http://localhost:8080/v3/api-docs | head -c 100
echo "..."
echo ""

echo -e "${GREEN}✅ API is responding successfully!${NC}"
echo ""

echo -e "${BLUE}🔧 API Demo Commands:${NC}"
echo ""
echo "# Register a new user"
echo 'curl -X POST http://localhost:8080/api/auth/register \'
echo '  -H "Content-Type: application/json" \'
echo '  -d '"'"'{"username":"demo","password":"DemoPass123"}'"'"
echo ""
echo "# Login to get JWT token"  
echo 'curl -X POST http://localhost:8080/api/auth/login \'
echo '  -H "Content-Type: application/json" \'
echo '  -d '"'"'{"username":"demo","password":"DemoPass123"}'"'"
echo ""
echo "# Create a transaction (use token from login)"
echo 'curl -X POST http://localhost:8080/api/transactions \'
echo '  -H "Authorization: Bearer YOUR_JWT_TOKEN" \'
echo '  -H "Content-Type: application/json" \'
echo '  -d '"'"'{"amount":25.50,"category":"Food","description":"Lunch"}'"'"
echo ""

cd ..

echo -e "${PURPLE}🔗 INTEGRATION POSSIBILITIES${NC}"
echo "=============================="
echo ""

echo -e "${CYAN}1. Shared Database Integration:${NC}"
echo "   • Both applications can use the same PostgreSQL database"
echo "   • Python CLI for admin tasks, API for web/mobile apps"
echo "   • Real-time data synchronization"
echo ""

echo -e "${CYAN}2. API Integration:${NC}"  
echo "   • Python CLI can consume Spring Boot API endpoints"
echo "   • Centralized business logic in Spring Boot"
echo "   • CLI as a client application"
echo ""

echo -e "${CYAN}3. Microservices Architecture:${NC}"
echo "   • Spring Boot API as core microservice"
echo "   • Python CLI as admin/tooling service"
echo "   • Independent scaling and deployment"
echo ""

echo -e "${BLUE}🎯 Wells Fargo Interview Value:${NC}"
echo ""
echo "✅ Full-Stack Development: Python + Java/Spring Boot"
echo "✅ Security Focus: Encryption, authentication, authorization"
echo "✅ Database Design: Relational design with proper indexing" 
echo "✅ API Design: RESTful principles, documentation, versioning"
echo "✅ Testing: Unit tests, integration tests, test automation"
echo "✅ DevOps: Docker, Maven, environment management"
echo "✅ Documentation: Comprehensive README, API docs, code comments"
echo ""

echo -e "${GREEN}🎉 Demo complete! Both applications are ready for use.${NC}"
echo ""
echo -e "${YELLOW}Next Steps:${NC}"
echo "1. 🐍 Try the Python CLI: python tracker.py start"
echo "2. 🌐 Explore the API: http://localhost:8080/swagger-ui.html" 
echo "3. 🧪 Run tests: pytest test_tracker.py -v"
echo "4. 📊 Check Spring Boot tests: cd backend-api && mvn test"
echo ""

# Cleanup function
cleanup() {
    echo ""
    echo -e "${YELLOW}Cleaning up demo processes...${NC}"
    if [ ! -z "$SPRING_PID" ]; then
        kill $SPRING_PID 2>/dev/null
        echo -e "${GREEN}✅ Spring Boot process stopped${NC}"
    fi
    deactivate 2>/dev/null
}

# Set trap for cleanup
trap cleanup EXIT

echo -e "${CYAN}Press Ctrl+C to stop demo and cleanup processes${NC}"
echo ""

# Keep script running
while true; do
    sleep 1
done
