package com.wellsfargo.interview.expensetracker.dto;

import java.math.BigDecimal;
import java.time.LocalDateTime;

/**
 * DTO for transaction responses
 */
public class TransactionResponse {
    
    private Long id;
    private BigDecimal amount;
    private String category;
    private String description; // This will be decrypted
    private LocalDateTime transactionDate;
    private LocalDateTime createdAt;
    private LocalDateTime updatedAt;
    
    // Constructors
    public TransactionResponse() {}
    
    public TransactionResponse(Long id, BigDecimal amount, String category, String description, 
                              LocalDateTime transactionDate, LocalDateTime createdAt, LocalDateTime updatedAt) {
        this.id = id;
        this.amount = amount;
        this.category = category;
        this.description = description;
        this.transactionDate = transactionDate;
        this.createdAt = createdAt;
        this.updatedAt = updatedAt;
    }
    
    // Getters and Setters
    public Long getId() {
        return id;
    }
    
    public void setId(Long id) {
        this.id = id;
    }
    
    public BigDecimal getAmount() {
        return amount;
    }
    
    public void setAmount(BigDecimal amount) {
        this.amount = amount;
    }
    
    public String getCategory() {
        return category;
    }
    
    public void setCategory(String category) {
        this.category = category;
    }
    
    public String getDescription() {
        return description;
    }
    
    public void setDescription(String description) {
        this.description = description;
    }
    
    public LocalDateTime getTransactionDate() {
        return transactionDate;
    }
    
    public void setTransactionDate(LocalDateTime transactionDate) {
        this.transactionDate = transactionDate;
    }
    
    public LocalDateTime getCreatedAt() {
        return createdAt;
    }
    
    public void setCreatedAt(LocalDateTime createdAt) {
        this.createdAt = createdAt;
    }
    
    public LocalDateTime getUpdatedAt() {
        return updatedAt;
    }
    
    public void setUpdatedAt(LocalDateTime updatedAt) {
        this.updatedAt = updatedAt;
    }
}
