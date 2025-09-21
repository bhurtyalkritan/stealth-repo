package com.wellsfargo.interview.expensetracker;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.security.config.annotation.web.configuration.EnableWebSecurity;
import org.springframework.transaction.annotation.EnableTransactionManagement;

/**
 * Secure Expense Tracker REST API
 * 
 * A comprehensive expense tracking application with:
 * - JWT-based authentication
 * - AES encryption for sensitive data
 * - RESTful API design
 * - Comprehensive security measures
 * 
 * Created for Wells Fargo Interview - September 2025
 */
@SpringBootApplication
@EnableWebSecurity
@EnableTransactionManagement
public class ExpenseTrackerApplication {

    public static void main(String[] args) {
        SpringApplication.run(ExpenseTrackerApplication.class, args);
        
        System.out.println("""
            
            🔒 Secure Expense Tracker API Started Successfully!
            
            📍 API Endpoints:
            • Swagger UI: http://localhost:8080/swagger-ui.html
            • API Docs: http://localhost:8080/v3/api-docs
            • Health Check: http://localhost:8080/actuator/health
            
            🔑 Authentication: JWT tokens required for protected endpoints
            💾 Database: H2 (dev) / PostgreSQL (prod)
            🔐 Security: AES-256 encryption + bcrypt password hashing
            
            Ready to receive requests! 🚀
            """);
    }
}
