package com.wellsfargo.interview.expensetracker.controller;

import com.wellsfargo.interview.expensetracker.dto.*;
import com.wellsfargo.interview.expensetracker.entity.User;
import com.wellsfargo.interview.expensetracker.service.TransactionService;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.Parameter;
import io.swagger.v3.oas.annotations.security.SecurityRequirement;
import io.swagger.v3.oas.annotations.tags.Tag;
import jakarta.validation.Valid;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageRequest;
import org.springframework.data.domain.Pageable;
import org.springframework.format.annotation.DateTimeFormat;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.security.core.annotation.AuthenticationPrincipal;
import org.springframework.web.bind.annotation.*;

import java.time.LocalDateTime;

/**
 * REST Controller for transaction operations
 */
@RestController
@RequestMapping("/api/transactions")
@Tag(name = "Transactions", description = "Transaction management operations")
@SecurityRequirement(name = "bearerAuth")
public class TransactionController {
    
    @Autowired
    private TransactionService transactionService;
    
    @PostMapping
    @Operation(summary = "Create a new transaction", description = "Creates a new expense transaction with encrypted description")
    public ResponseEntity<TransactionResponse> createTransaction(
            @AuthenticationPrincipal User user,
            @Valid @RequestBody TransactionRequest request) {
        
        TransactionResponse response = transactionService.createTransaction(user, request);
        return ResponseEntity.status(HttpStatus.CREATED).body(response);
    }
    
    @GetMapping
    @Operation(summary = "Get transactions", description = "Retrieve transactions with optional filtering and pagination")
    public ResponseEntity<Page<TransactionResponse>> getTransactions(
            @AuthenticationPrincipal User user,
            @Parameter(description = "Filter by category") @RequestParam(required = false) String category,
            @Parameter(description = "Start date filter (ISO format)") 
            @RequestParam(required = false) @DateTimeFormat(iso = DateTimeFormat.ISO.DATE_TIME) LocalDateTime startDate,
            @Parameter(description = "End date filter (ISO format)") 
            @RequestParam(required = false) @DateTimeFormat(iso = DateTimeFormat.ISO.DATE_TIME) LocalDateTime endDate,
            @Parameter(description = "Page number (0-based)") @RequestParam(defaultValue = "0") int page,
            @Parameter(description = "Page size") @RequestParam(defaultValue = "20") int size) {
        
        Pageable pageable = PageRequest.of(page, size);
        Page<TransactionResponse> transactions = transactionService.getTransactions(
            user, category, startDate, endDate, pageable);
        
        return ResponseEntity.ok(transactions);
    }
    
    @GetMapping("/{id}")
    @Operation(summary = "Get transaction by ID", description = "Retrieve a specific transaction by its ID")
    public ResponseEntity<TransactionResponse> getTransactionById(
            @AuthenticationPrincipal User user,
            @Parameter(description = "Transaction ID") @PathVariable Long id) {
        
        return transactionService.getTransactionById(user, id)
            .map(transaction -> ResponseEntity.ok().body(transaction))
            .orElse(ResponseEntity.notFound().build());
    }
    
    @PutMapping("/{id}")
    @Operation(summary = "Update transaction", description = "Update an existing transaction")
    public ResponseEntity<TransactionResponse> updateTransaction(
            @AuthenticationPrincipal User user,
            @Parameter(description = "Transaction ID") @PathVariable Long id,
            @Valid @RequestBody TransactionRequest request) {
        
        return transactionService.updateTransaction(user, id, request)
            .map(transaction -> ResponseEntity.ok().body(transaction))
            .orElse(ResponseEntity.notFound().build());
    }
    
    @DeleteMapping("/{id}")
    @Operation(summary = "Delete transaction", description = "Delete a transaction by ID")
    public ResponseEntity<Void> deleteTransaction(
            @AuthenticationPrincipal User user,
            @Parameter(description = "Transaction ID") @PathVariable Long id) {
        
        boolean deleted = transactionService.deleteTransaction(user, id);
        return deleted ? ResponseEntity.noContent().build() : ResponseEntity.notFound().build();
    }
    
    @GetMapping("/stats")
    @Operation(summary = "Get user statistics", description = "Retrieve spending statistics for the authenticated user")
    public ResponseEntity<UserStatsResponse> getUserStats(@AuthenticationPrincipal User user) {
        UserStatsResponse stats = transactionService.getUserStats(user);
        return ResponseEntity.ok(stats);
    }
    
    @GetMapping("/reports/monthly")
    @Operation(summary = "Generate monthly report", description = "Generate a detailed monthly spending report")
    public ResponseEntity<MonthlyReportResponse> getMonthlyReport(
            @AuthenticationPrincipal User user,
            @Parameter(description = "Year") @RequestParam int year,
            @Parameter(description = "Month (1-12)") @RequestParam int month) {
        
        if (month < 1 || month > 12) {
            return ResponseEntity.badRequest().build();
        }
        
        MonthlyReportResponse report = transactionService.generateMonthlyReport(user, year, month);
        return ResponseEntity.ok(report);
    }
}
