package com.wellsfargo.interview.expensetracker.service;

import com.wellsfargo.interview.expensetracker.dto.*;
import com.wellsfargo.interview.expensetracker.entity.Transaction;
import com.wellsfargo.interview.expensetracker.entity.User;
import com.wellsfargo.interview.expensetracker.repository.TransactionRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageRequest;
import org.springframework.data.domain.Pageable;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.math.BigDecimal;
import java.math.RoundingMode;
import java.time.LocalDateTime;
import java.time.Month;
import java.util.ArrayList;
import java.util.List;
import java.util.Optional;

/**
 * Service for handling transaction operations
 */
@Service
@Transactional
public class TransactionService {
    
    @Autowired
    private TransactionRepository transactionRepository;
    
    @Autowired
    private EncryptionService encryptionService;
    
    /**
     * Create a new transaction
     */
    public TransactionResponse createTransaction(User user, TransactionRequest request) {
        Transaction transaction = new Transaction();
        transaction.setUser(user);
        transaction.setAmount(request.getAmount());
        transaction.setCategory(request.getCategory());
        transaction.setTransactionDate(request.getTransactionDate() != null ? 
            request.getTransactionDate() : LocalDateTime.now());
        
        // Encrypt description if provided
        if (request.getDescription() != null && !request.getDescription().isEmpty()) {
            String encryptedDescription = encryptionService.encrypt(request.getDescription());
            transaction.setEncryptedDescription(encryptedDescription);
        }
        
        Transaction savedTransaction = transactionRepository.save(transaction);
        return convertToResponse(savedTransaction);
    }
    
    /**
     * Get transactions with filtering and pagination
     */
    @Transactional(readOnly = true)
    public Page<TransactionResponse> getTransactions(User user, String category, 
                                                   LocalDateTime startDate, LocalDateTime endDate, 
                                                   Pageable pageable) {
        Page<Transaction> transactions = transactionRepository.findByUserWithFilters(
            user, category, startDate, endDate, pageable);
        
        return transactions.map(this::convertToResponse);
    }
    
    /**
     * Get transaction by ID
     */
    @Transactional(readOnly = true)
    public Optional<TransactionResponse> getTransactionById(User user, Long id) {
        return transactionRepository.findById(id)
            .filter(transaction -> transaction.getUser().getId().equals(user.getId()))
            .map(this::convertToResponse);
    }
    
    /**
     * Update transaction
     */
    public Optional<TransactionResponse> updateTransaction(User user, Long id, TransactionRequest request) {
        return transactionRepository.findById(id)
            .filter(transaction -> transaction.getUser().getId().equals(user.getId()))
            .map(transaction -> {
                transaction.setAmount(request.getAmount());
                transaction.setCategory(request.getCategory());
                if (request.getTransactionDate() != null) {
                    transaction.setTransactionDate(request.getTransactionDate());
                }
                
                // Update encrypted description
                if (request.getDescription() != null) {
                    if (request.getDescription().isEmpty()) {
                        transaction.setEncryptedDescription(null);
                    } else {
                        String encryptedDescription = encryptionService.encrypt(request.getDescription());
                        transaction.setEncryptedDescription(encryptedDescription);
                    }
                }
                
                Transaction savedTransaction = transactionRepository.save(transaction);
                return convertToResponse(savedTransaction);
            });
    }
    
    /**
     * Delete transaction
     */
    public boolean deleteTransaction(User user, Long id) {
        return transactionRepository.findById(id)
            .filter(transaction -> transaction.getUser().getId().equals(user.getId()))
            .map(transaction -> {
                transactionRepository.delete(transaction);
                return true;
            })
            .orElse(false);
    }
    
    /**
     * Generate monthly report
     */
    @Transactional(readOnly = true)
    public MonthlyReportResponse generateMonthlyReport(User user, int year, int month) {
        LocalDateTime startDate = LocalDateTime.of(year, month, 1, 0, 0, 0);
        LocalDateTime endDate = startDate.plusMonths(1).minusSeconds(1);
        
        Page<Transaction> transactions = transactionRepository.findByUserAndDateRange(
            user, startDate, endDate, PageRequest.of(0, Integer.MAX_VALUE));
        
        List<Transaction> transactionList = transactions.getContent();
        
        if (transactionList.isEmpty()) {
            return new MonthlyReportResponse(year, month, Month.of(month).name(), 
                BigDecimal.ZERO, 0, BigDecimal.ZERO);
        }
        
        // Calculate totals
        BigDecimal totalSpent = transactionList.stream()
            .map(Transaction::getAmount)
            .reduce(BigDecimal.ZERO, BigDecimal::add);
        
        BigDecimal averageTransaction = totalSpent.divide(
            BigDecimal.valueOf(transactionList.size()), 2, RoundingMode.HALF_UP);
        
        MonthlyReportResponse report = new MonthlyReportResponse(
            year, month, Month.of(month).name(), 
            totalSpent, transactionList.size(), averageTransaction);
        
        // Calculate category breakdown
        List<MonthlyReportResponse.CategorySpending> categoryBreakdown = new ArrayList<>();
        transactionList.stream()
            .collect(java.util.stream.Collectors.groupingBy(
                Transaction::getCategory,
                java.util.stream.Collectors.reducing(BigDecimal.ZERO, 
                    Transaction::getAmount, BigDecimal::add)))
            .entrySet().stream()
            .sorted((e1, e2) -> e2.getValue().compareTo(e1.getValue()))
            .forEach(entry -> {
                String category = entry.getKey();
                BigDecimal amount = entry.getValue();
                double percentage = amount.divide(totalSpent, 4, RoundingMode.HALF_UP)
                    .multiply(BigDecimal.valueOf(100)).doubleValue();
                
                long count = transactionList.stream()
                    .filter(t -> t.getCategory().equals(category))
                    .count();
                
                categoryBreakdown.add(new MonthlyReportResponse.CategorySpending(
                    category, amount, percentage, (int) count));
            });
        
        report.setCategoryBreakdown(categoryBreakdown);
        
        return report;
    }
    
    /**
     * Get user statistics
     */
    @Transactional(readOnly = true)
    public UserStatsResponse getUserStats(User user) {
        BigDecimal totalSpent = transactionRepository.getTotalSpendingByUser(user);
        long transactionCount = transactionRepository.countByUser(user);
        BigDecimal averageAmount = transactionRepository.getAverageTransactionAmount(user);
        
        List<Transaction> recentTransactions = transactionRepository
            .findTop10ByUserOrderByTransactionDateDesc(user, PageRequest.of(0, 10));
        
        List<TransactionResponse> recentTransactionResponses = recentTransactions.stream()
            .map(this::convertToResponse)
            .toList();
        
        return new UserStatsResponse(totalSpent, transactionCount, 
            averageAmount != null ? averageAmount : BigDecimal.ZERO, 
            recentTransactionResponses);
    }
    
    /**
     * Convert Transaction entity to TransactionResponse DTO
     */
    private TransactionResponse convertToResponse(Transaction transaction) {
        String decryptedDescription = null;
        if (transaction.getEncryptedDescription() != null) {
            decryptedDescription = encryptionService.decrypt(transaction.getEncryptedDescription());
        }
        
        return new TransactionResponse(
            transaction.getId(),
            transaction.getAmount(),
            transaction.getCategory(),
            decryptedDescription,
            transaction.getTransactionDate(),
            transaction.getCreatedAt(),
            transaction.getUpdatedAt()
        );
    }
}
