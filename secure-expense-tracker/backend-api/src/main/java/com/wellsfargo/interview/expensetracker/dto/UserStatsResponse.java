package com.wellsfargo.interview.expensetracker.dto;

import java.math.BigDecimal;
import java.util.List;

/**
 * DTO for user statistics
 */
public class UserStatsResponse {
    
    private BigDecimal totalSpent;
    private long totalTransactions;
    private BigDecimal averageTransaction;
    private List<TransactionResponse> recentTransactions;
    
    // Constructors
    public UserStatsResponse() {}
    
    public UserStatsResponse(BigDecimal totalSpent, long totalTransactions, 
                            BigDecimal averageTransaction, List<TransactionResponse> recentTransactions) {
        this.totalSpent = totalSpent;
        this.totalTransactions = totalTransactions;
        this.averageTransaction = averageTransaction;
        this.recentTransactions = recentTransactions;
    }
    
    // Getters and Setters
    public BigDecimal getTotalSpent() {
        return totalSpent;
    }
    
    public void setTotalSpent(BigDecimal totalSpent) {
        this.totalSpent = totalSpent;
    }
    
    public long getTotalTransactions() {
        return totalTransactions;
    }
    
    public void setTotalTransactions(long totalTransactions) {
        this.totalTransactions = totalTransactions;
    }
    
    public BigDecimal getAverageTransaction() {
        return averageTransaction;
    }
    
    public void setAverageTransaction(BigDecimal averageTransaction) {
        this.averageTransaction = averageTransaction;
    }
    
    public List<TransactionResponse> getRecentTransactions() {
        return recentTransactions;
    }
    
    public void setRecentTransactions(List<TransactionResponse> recentTransactions) {
        this.recentTransactions = recentTransactions;
    }
}
