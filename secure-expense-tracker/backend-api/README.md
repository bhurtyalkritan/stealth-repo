# Expense Tracker REST API

Spring Boot REST API for expense tracking with JWT authentication and data encryption.

Features:
- REST endpoints for expense management
- JWT authentication
- AES encryption for sensitive data
- H2 database (dev) / PostgreSQL (prod)
- Swagger documentation

## Project Structure

```
backend-api/
├── src/main/java/com/wellsfargo/interview/expensetracker/
│   ├── controller/     # REST controllers
│   ├── service/        # Business logic
│   ├── repository/     # Data access
│   ├── entity/         # JPA entities
│   ├── dto/           # Request/response objects
│   ├── config/        # Security & API config
│   └── exception/     # Error handling
├── src/main/resources/
│   └── application.yml
└── pom.xml
```

## Quick Start

**Requirements:** Java 17+, Maven 3.6+

```bash
cd backend-api
mvn spring-boot:run
```

**Access:**
- API: http://localhost:8080/api
- Swagger: http://localhost:8080/swagger-ui.html
- H2 Console: http://localhost:8080/h2-console

**Test it:**
```bash
# Register
curl -X POST http://localhost:8080/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username":"test","password":"TestPass123"}'

# Login
curl -X POST http://localhost:8080/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"test","password":"TestPass123"}'
```

## API Endpoints

**Auth:**
- `POST /api/auth/register` - Register user
- `POST /api/auth/login` - Login

**Transactions:**
- `GET /api/transactions` - List transactions
- `POST /api/transactions` - Create transaction
- `PUT /api/transactions/{id}` - Update transaction
- `DELETE /api/transactions/{id}` - Delete transaction

**Reports:**
- `GET /api/transactions/stats` - Spending stats
- `GET /api/transactions/reports/monthly` - Monthly report

## Security

- JWT tokens (24-hour expiry)
- AES-256 encryption for transaction descriptions
- Password requirements: 8+ chars, mixed case, numbers
- Account lockout after 3 failed attempts

## Database

Tables: users, transactions, categories
- User authentication with lockout tracking
- Encrypted transaction descriptions
- Foreign key relationships

## Configuration

**Development:** H2 in-memory database
**Production:** PostgreSQL with environment variables:
- `DB_USERNAME`
- `DB_PASSWORD` 
- `JWT_SECRET`

## Testing

```bash
mvn test
```

## Integration with Python CLI

Can work with the Python CLI through:
1. Shared database (same PostgreSQL instance)
2. API calls from Python to Spring Boot endpoints

## Docker Deployment

```bash
mvn clean package
docker build -t expense-tracker-api .
docker-compose up -d
```

## Key Features

- RESTful API design with proper HTTP methods
- Spring Boot with layered architecture
- JPA/Hibernate for database operations
- JWT authentication and AES encryption
- Global exception handling
- Swagger API documentation
- Docker deployment support
