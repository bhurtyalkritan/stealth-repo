# 🔒 Secure Expense Tracker - Full Stack Edition

A comprehensive, secure expense tracking solution featuring both a Python CLI application and a Spring Boot REST API, built for the Wells Fargo interview process.

## 🏗️ Architecture Overview

This project demonstrates full-stack development capabilities with **two complementary applications**:

### 🐍 Python CLI Application
- **Interactive Terminal Interface**: Rich CLI with colorful menus and ASCII charts
- **Local Database**: SQLite with SQLAlchemy ORM
- **Personal Use**: Perfect for individual expense tracking
- **Fast Setup**: Single command installation and execution

### ☕ Spring Boot REST API
- **Enterprise REST API**: RESTful endpoints with comprehensive documentation
- **JWT Authentication**: Secure token-based authentication
- **Production Database**: H2 (development) / PostgreSQL (production)
- **Scalable Architecture**: Microservice-ready, stateless design
- **API Documentation**: Auto-generated Swagger/OpenAPI docs

### 🔗 Integration Capabilities
- **Shared Database**: Both applications can work with the same data
- **API Integration**: Python CLI can consume Spring Boot endpoints  
- **Hybrid Usage**: Use CLI for admin tasks, API for web/mobile apps

## 🚀 Features

### Core Functionality
- ✅ **Add Transactions**: Record expenses with amount, category, description, and date
- ✅ **View Transactions**: List transactions with filtering by category and date range
- ✅ **Monthly Reports**: Visual ASCII charts showing spending breakdown
- ✅ **Category Management**: Pre-set categories + custom user-defined categories
- ✅ **Spending Analytics**: Daily averages, totals, and transaction summaries

### Security Features
- 🔐 **User Authentication**: Secure login system with bcrypt password hashing
- 🔒 **Data Encryption**: AES encryption for sensitive transaction data using `cryptography` library
- 🛡️ **Account Protection**: Account lockout after 3 failed login attempts (30-minute lockout)
- 🔑 **Password Validation**: Strong password requirements (8+ chars, uppercase, lowercase, numbers)

### Modern CLI Experience
- 🎨 **Rich Interface**: Beautiful CLI with colors, tables, and progress indicators using `rich` library
- 📊 **Visual Reports**: ASCII bar charts for spending analysis
- 🔍 **Smart Filtering**: Filter transactions by category, date range
- 📤 **Export Options**: Export to CSV and PDF formats
- ⚡ **Fast Navigation**: Intuitive menu system with input validation

### Data Storage
- 💾 **SQLAlchemy ORM**: Robust database operations with relationships
- 🗃️ **SQLite Database**: Lightweight, portable data storage
- 🔄 **Database Backup**: Built-in backup functionality

## 🛠️ Installation & Setup

### Prerequisites
- **Python 3.8+** (for CLI application)
- **Java 17+** (for Spring Boot API)
- **Maven 3.6+** (for Spring Boot build)
- **PostgreSQL** (optional, for production API)

### 🚀 Quick Start (Full Stack)

```bash
# 1. Navigate to project directory
cd secure-expense-tracker

# 2. Run full-stack setup (sets up both Python CLI and Spring Boot API)
./setup-full-stack.sh

# 3a. Start Python CLI Application
source venv/bin/activate
python tracker.py start

# 3b. Start Spring Boot API (in another terminal)
cd backend-api
mvn spring-boot:run
# API available at: http://localhost:8080
# Swagger UI: http://localhost:8080/swagger-ui.html
```

### 🐍 Python CLI Only Setup

```bash
# Quick CLI-only setup
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python tracker.py start
```

### ☕ Spring Boot API Only Setup

```bash
# Quick API-only setup
cd backend-api
mvn clean compile
mvn spring-boot:run
```

### First Runw
1. The app will initialize the database automatically
2. Create your account (username + strong password)
3. Start tracking your expenses!

## 📖 Usage Guide

### Starting the Application
```bash
python tracker.py start
```

### Main Menu Options
1. **💰 Add Transaction** - Record a new expense
2. **📊 View Transactions** - Browse and filter transactions
3. **📈 Monthly Report** - Visual spending analysis
4. **📅 Spending Summary** - Statistics for custom date ranges
5. **🏷️ Manage Categories** - Add custom expense categories
6. **📤 Export Data** - Export to CSV or PDF
7. **⚙️ Settings** - Account management
8. **🚪 Logout** - Secure logout

### Example Usage Flow

```bash
$ python tracker.py start

🔒 Secure Expense Tracker
Your finances, encrypted and secure
────────────────────────────────────

Authentication Required
1. Login
2. Sign Up
3. Exit
> 2

Choose username: john_doe
Choose password: [hidden]
Confirm password: [hidden]
✅ Account created successfully for john_doe!

📋 Main Menu
1. 💰 Add Transaction
2. 📊 View Transactions
...
> 1

💰 Add New Transaction
Amount ($): 45.50
Category (Food): Food
Description (optional): Lunch at downtown cafe
Date (YYYY-MM-DD, or press Enter for today): 
✅ Transaction saved: $45.50 for Food 🔐

> 3

📊 Monthly Report - September 2025
Total Spent: $245.50

Food         ████████████████░░░░  $145.50 (59.3%)
Transport    ██████░░░░░░░░░░░░░░   $65.00 (26.5%)
Other        ███░░░░░░░░░░░░░░░░░   $35.00 (14.2%)
```

## 🧩 Architecture & Code Structure

```
secure-expense-tracker/
├── 🐍 Python CLI Application
│   ├── tracker.py              # 🚀 Main CLI entry point
│   ├── auth.py                 # 🔐 Authentication & user management
│   ├── db.py                   # 💾 SQLAlchemy models & database
│   ├── crypto.py               # 🔒 AES encryption utilities
│   ├── expenses.py             # 💰 Core expense tracking logic
│   ├── ui.py                   # 🎨 Rich-based UI components
│   ├── export.py               # 📤 CSV/PDF export functionality
│   ├── test_tracker.py         # 🧪 Unit tests
│   └── requirements.txt        # 📦 Python dependencies
│
├── ☕ Spring Boot REST API
│   ├── backend-api/
│   │   ├── src/main/java/com/wellsfargo/interview/expensetracker/
│   │   │   ├── ExpenseTrackerApplication.java    # 🚀 Spring Boot main class
│   │   │   ├── controller/                       # 🌐 REST Controllers
│   │   │   │   ├── TransactionController.java
│   │   │   │   └── AuthController.java
│   │   │   ├── service/                          # 🔧 Business Logic
│   │   │   │   ├── TransactionService.java
│   │   │   │   ├── UserService.java
│   │   │   │   └── EncryptionService.java
│   │   │   ├── repository/                       # 🗄️ Data Access Layer
│   │   │   │   ├── TransactionRepository.java
│   │   │   │   ├── UserRepository.java
│   │   │   │   └── CategoryRepository.java
│   │   │   ├── entity/                          # 📊 JPA Entities
│   │   │   │   ├── User.java
│   │   │   │   ├── Transaction.java
│   │   │   │   └── Category.java
│   │   │   ├── dto/                             # 📦 Data Transfer Objects
│   │   │   ├── config/                          # ⚙️ Configuration
│   │   │   └── exception/                       # ⚠️ Exception Handling
│   │   ├── src/main/resources/
│   │   │   └── application.yml                  # 📋 App Configuration
│   │   ├── pom.xml                             # 📦 Maven Dependencies
│   │   └── README.md                           # 📖 API Documentation
│
├── 🔧 Setup & Configuration
│   ├── setup-full-stack.sh        # 🚀 Complete setup script
│   ├── setup.sh                   # 🐍 Python CLI setup only
│   └── README.md                  # 📖 This comprehensive guide
```

### Key Components

**tracker.py** - Main application controller
- CLI command handling with `typer`
- User authentication flow
- Menu navigation and user input handling

**auth.py** - Security & authentication
- bcrypt password hashing with salt
- Account lockout protection
- Password strength validation

**db.py** - Data layer
- SQLAlchemy ORM models (User, Transaction, Category)
- Database relationships and constraints
- Session management

**crypto.py** - Encryption layer
- AES encryption using `cryptography.Fernet`
- Secure key generation and storage
- Transparent encrypt/decrypt operations

**expenses.py** - Business logic
- Transaction CRUD operations
- Filtering and search functionality
- Report generation and analytics

**ui.py** - User interface
- Rich console formatting
- Input validation and error handling
- Interactive prompts and menus

## 🔧 Extending the Application

### Adding New Features

#### 1. New Transaction Fields
```python
# In db.py - Add new column to Transaction model
class Transaction(Base):
    # ...existing fields...
    location = Column(String(200), nullable=True)
    receipt_url = Column(String(500), nullable=True)

# In expenses.py - Update add_transaction function
def add_transaction(user, amount, category, description, location=None):
    # Add location handling
    encrypted_location = encrypt_text(location) if location else ""
    # ...rest of function
```

#### 2. Advanced Reporting
```python
# In expenses.py - Add new report type
def yearly_report(user: User, year: int):
    """Generate yearly spending analysis."""
    # Implementation here
    
def category_trends(user: User, months: int = 6):
    """Show spending trends by category over time."""
    # Implementation here
```

#### 3. Budget Management
```python
# In db.py - New Budget model
class Budget(Base):
    __tablename__ = 'budgets'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    category = Column(String(100))
    monthly_limit = Column(Float)
    # ...
```

#### 4. Data Import/Sync
```python
# In export.py - Add import functionality
def import_from_csv(user, filename: str):
    """Import transactions from CSV file."""
    # Implementation here

def sync_with_bank_api(user, bank_credentials):
    """Sync with bank API (mock implementation)."""
    # Implementation here
```

### Testing Extensions

Always add tests for new features:

```python
# In test_tracker.py
class TestNewFeature:
    def test_new_functionality(self):
        """Test description."""
        # Test implementation
        assert expected_result == actual_result
```

### UI Enhancements

For more interactive UI, consider upgrading to `textual`:

```python
# Alternative: Use textual for full TUI
from textual.app import App
from textual.widgets import Button, Input, DataTable

class ExpenseTrackerApp(App):
    def compose(self):
        yield Button("Add Transaction", id="add")
        yield DataTable()
    # ...
```

## 🧪 Testing

Run the test suite:

```bash
# Run all tests
python -m pytest test_tracker.py -v

# Run specific test class
python -m pytest test_tracker.py::TestAuth -v

# Run with coverage
pip install pytest-cov
python -m pytest test_tracker.py --cov=. --cov-report=html
```

### Test Coverage Areas
- ✅ Authentication (signup, login, password hashing)
- ✅ Encryption/decryption
- ✅ Transaction operations
- ✅ Database operations
- 🔄 UI components (manual testing)
- 🔄 Export functionality (manual testing)

## 🚀 Deployment & Distribution

### Creating Executable
```bash
# Install PyInstaller
pip install pyinstaller

# Create standalone executable
pyinstaller --onefile --name expense-tracker tracker.py

# Executable will be in dist/ folder
./dist/expense-tracker start
```

### Docker Deployment
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "tracker.py", "start"]
```

## 🎯 Interview Highlights

This full-stack project demonstrates comprehensive software engineering skills:

### 🐍 Python Development
- **CLI Application Design**: Interactive terminal UI with Rich library
- **SQLAlchemy ORM**: Database relationships and query optimization  
- **Encryption**: AES-256 encryption for sensitive data
- **Testing**: Comprehensive unit tests with pytest
- **Package Management**: Virtual environments and dependency management

### ☕ Java/Spring Boot Development  
- **RESTful API Design**: Proper HTTP methods, status codes, resource naming
- **Spring Boot Ecosystem**: Auto-configuration, dependency injection, profiles
- **JPA/Hibernate**: Entity relationships, repository pattern, query methods
- **JWT Security**: Token-based authentication with Spring Security
- **Enterprise Patterns**: Layered architecture, DTO pattern, exception handling

### 🔒 Security Implementation
- **Authentication**: Secure login with account lockout protection
- **Encryption**: AES-256 for data at rest, bcrypt for passwords  
- **Authorization**: JWT tokens with proper validation
- **Input Validation**: Comprehensive data validation and sanitization
- **Security Headers**: CSRF protection, CORS configuration

### 🏗️ Architecture & Design
- **Full-Stack Integration**: Two applications that can work together
- **Database Design**: Normalized schema with proper indexing
- **API Documentation**: Auto-generated Swagger/OpenAPI documentation
- **Configuration Management**: Environment-specific configurations
- **Error Handling**: Comprehensive exception handling and logging

### 🚀 Production Readiness
- **Containerization**: Docker support for deployment
- **Monitoring**: Health checks and metrics with Spring Actuator
- **Testing Strategy**: Unit tests, integration tests, test profiles
- **CI/CD Ready**: Maven build, automated testing, deployment scripts

### 💼 Business Value
- **Real-World Application**: Practical expense tracking solution
- **Scalability**: Microservice architecture, stateless design
- **Maintainability**: Clean code, comprehensive documentation
- **Extensibility**: Plugin architecture for new features

## 🐛 Troubleshooting

### Common Issues

**Import Errors**
```bash
# Make sure virtual environment is activated
source venv/bin/activate
pip install -r requirements.txt
```

**Database Issues**
```bash
# Reset database
rm tracker.db secret.key
python tracker.py init
```

**Permission Errors**
```bash
# On macOS/Linux, ensure script is executable
chmod +x tracker.py
```

### Getting Help

1. Check the error message carefully
2. Verify all dependencies are installed
3. Ensure Python 3.8+ is being used
4. Try resetting the database for data-related issues

## 🔮 Future Enhancements

### Phase 2 Features
- [ ] **Web Interface**: Flask/FastAPI web version
- [ ] **Mobile App**: React Native companion app
- [ ] **Cloud Sync**: Multi-device synchronization
- [ ] **Advanced Analytics**: Machine learning insights
- [ ] **Integration**: Bank API connections
- [ ] **Notifications**: Budget alerts and reminders
- [ ] **Team Features**: Shared household expenses
- [ ] **Receipt Scanning**: OCR integration
- [ ] **Multi-Currency**: International expense tracking
- [ ] **Investment Tracking**: Portfolio management

### Technical Improvements
- [ ] **GraphQL API**: Modern API layer
- [ ] **Redis Caching**: Performance optimization
- [ ] **PostgreSQL**: Production database
- [ ] **Docker Compose**: Multi-service deployment
- [ ] **CI/CD Pipeline**: Automated testing and deployment
- [ ] **Monitoring**: Application performance monitoring
- [ ] **Logging**: Structured logging with ELK stack

---

**Created for Wells Fargo Interview - September 2025** 🚀

*This project showcases practical software engineering skills, security awareness, and attention to user experience - all critical for modern financial applications.*
