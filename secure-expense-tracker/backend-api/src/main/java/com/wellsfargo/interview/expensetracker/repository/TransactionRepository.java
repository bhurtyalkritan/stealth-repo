package com.wellsfargo.interview.expensetracker.repository;

import com.wellsfargo.interview.expensetracker.entity.Transaction;
import com.wellsfargo.interview.expensetracker.entity.User;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.math.BigDecimal;
import java.time.LocalDateTime;
import java.util.List;

/**
 * Repository interface for Transaction entity operations
 */
@Repository
public interface TransactionRepository extends JpaRepository<Transaction, Long> {
    
    /**
     * Find transactions by user with pagination
     */
    Page<Transaction> findByUserOrderByTransactionDateDesc(User user, Pageable pageable);
    
    /**
     * Find transactions by user and category
     */
    Page<Transaction> findByUserAndCategoryContainingIgnoreCaseOrderByTransactionDateDesc(
            User user, String category, Pageable pageable);
    
    /**
     * Find transactions by user within date range
     */
    @Query("SELECT t FROM Transaction t WHERE t.user = :user AND t.transactionDate BETWEEN :startDate AND :endDate ORDER BY t.transactionDate DESC")
    Page<Transaction> findByUserAndDateRange(
            @Param("user") User user,
            @Param("startDate") LocalDateTime startDate,
            @Param("endDate") LocalDateTime endDate,
            Pageable pageable);
    
    /**
     * Find transactions by user, category, and date range
     */
    @Query("SELECT t FROM Transaction t WHERE t.user = :user " +
           "AND (:category IS NULL OR LOWER(t.category) LIKE LOWER(CONCAT('%', :category, '%'))) " +
           "AND (:startDate IS NULL OR t.transactionDate >= :startDate) " +
           "AND (:endDate IS NULL OR t.transactionDate <= :endDate) " +
           "ORDER BY t.transactionDate DESC")
    Page<Transaction> findByUserWithFilters(
            @Param("user") User user,
            @Param("category") String category,
            @Param("startDate") LocalDateTime startDate,
            @Param("endDate") LocalDateTime endDate,
            Pageable pageable);
    
    /**
     * Get total spending by user
     */
    @Query("SELECT COALESCE(SUM(t.amount), 0) FROM Transaction t WHERE t.user = :user")
    BigDecimal getTotalSpendingByUser(@Param("user") User user);
    
    /**
     * Get spending by category for a user
     */
    @Query("SELECT t.category, SUM(t.amount) FROM Transaction t WHERE t.user = :user GROUP BY t.category ORDER BY SUM(t.amount) DESC")
    List<Object[]> getSpendingByCategory(@Param("user") User user);
    
    /**
     * Get monthly spending summary
     */
    @Query("SELECT YEAR(t.transactionDate), MONTH(t.transactionDate), SUM(t.amount) " +
           "FROM Transaction t WHERE t.user = :user " +
           "AND t.transactionDate >= :startDate " +
           "GROUP BY YEAR(t.transactionDate), MONTH(t.transactionDate) " +
           "ORDER BY YEAR(t.transactionDate) DESC, MONTH(t.transactionDate) DESC")
    List<Object[]> getMonthlySpending(@Param("user") User user, @Param("startDate") LocalDateTime startDate);
    
    /**
     * Get recent transactions for dashboard
     */
    @Query("SELECT t FROM Transaction t WHERE t.user = :user ORDER BY t.transactionDate DESC")
    List<Transaction> findTop10ByUserOrderByTransactionDateDesc(@Param("user") User user, Pageable pageable);
    
    /**
     * Count transactions by user
     */
    long countByUser(User user);
    
    /**
     * Get average transaction amount for user
     */
    @Query("SELECT AVG(t.amount) FROM Transaction t WHERE t.user = :user")
    BigDecimal getAverageTransactionAmount(@Param("user") User user);
}
