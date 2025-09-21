package com.wellsfargo.interview.expensetracker.dto;

import java.math.BigDecimal;
import java.util.List;
import java.util.Map;

/**
 * DTO for monthly spending reports
 */
public class MonthlyReportResponse {
    
    private int year;
    private int month;
    private String monthName;
    private BigDecimal totalSpent;
    private int transactionCount;
    private BigDecimal averageTransaction;
    private List<CategorySpending> categoryBreakdown;
    private Map<String, BigDecimal> dailySpending;
    
    // Constructors
    public MonthlyReportResponse() {}
    
    public MonthlyReportResponse(int year, int month, String monthName, BigDecimal totalSpent, 
                                int transactionCount, BigDecimal averageTransaction) {
        this.year = year;
        this.month = month;
        this.monthName = monthName;
        this.totalSpent = totalSpent;
        this.transactionCount = transactionCount;
        this.averageTransaction = averageTransaction;
    }
    
    // Inner class for category spending
    public static class CategorySpending {
        private String category;
        private BigDecimal amount;
        private double percentage;
        private int transactionCount;
        
        public CategorySpending() {}
        
        public CategorySpending(String category, BigDecimal amount, double percentage, int transactionCount) {
            this.category = category;
            this.amount = amount;
            this.percentage = percentage;
            this.transactionCount = transactionCount;
        }
        
        // Getters and Setters
        public String getCategory() {
            return category;
        }
        
        public void setCategory(String category) {
            this.category = category;
        }
        
        public BigDecimal getAmount() {
            return amount;
        }
        
        public void setAmount(BigDecimal amount) {
            this.amount = amount;
        }
        
        public double getPercentage() {
            return percentage;
        }
        
        public void setPercentage(double percentage) {
            this.percentage = percentage;
        }
        
        public int getTransactionCount() {
            return transactionCount;
        }
        
        public void setTransactionCount(int transactionCount) {
            this.transactionCount = transactionCount;
        }
    }
    
    // Getters and Setters
    public int getYear() {
        return year;
    }
    
    public void setYear(int year) {
        this.year = year;
    }
    
    public int getMonth() {
        return month;
    }
    
    public void setMonth(int month) {
        this.month = month;
    }
    
    public String getMonthName() {
        return monthName;
    }
    
    public void setMonthName(String monthName) {
        this.monthName = monthName;
    }
    
    public BigDecimal getTotalSpent() {
        return totalSpent;
    }
    
    public void setTotalSpent(BigDecimal totalSpent) {
        this.totalSpent = totalSpent;
    }
    
    public int getTransactionCount() {
        return transactionCount;
    }
    
    public void setTransactionCount(int transactionCount) {
        this.transactionCount = transactionCount;
    }
    
    public BigDecimal getAverageTransaction() {
        return averageTransaction;
    }
    
    public void setAverageTransaction(BigDecimal averageTransaction) {
        this.averageTransaction = averageTransaction;
    }
    
    public List<CategorySpending> getCategoryBreakdown() {
        return categoryBreakdown;
    }
    
    public void setCategoryBreakdown(List<CategorySpending> categoryBreakdown) {
        this.categoryBreakdown = categoryBreakdown;
    }
    
    public Map<String, BigDecimal> getDailySpending() {
        return dailySpending;
    }
    
    public void setDailySpending(Map<String, BigDecimal> dailySpending) {
        this.dailySpending = dailySpending;
    }
}
