package com.wellsfargo.interview.expensetracker.repository;

import com.wellsfargo.interview.expensetracker.entity.User;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.util.Optional;

/**
 * Repository interface for User entity operations
 */
@Repository
public interface UserRepository extends JpaRepository<User, Long> {
    
    /**
     * Find user by username
     */
    Optional<User> findByUsername(String username);
    
    /**
     * Check if username exists
     */
    boolean existsByUsername(String username);
    
    /**
     * Find user by username with transactions (for analytics)
     */
    @Query("SELECT u FROM User u LEFT JOIN FETCH u.transactions WHERE u.username = :username")
    Optional<User> findByUsernameWithTransactions(@Param("username") String username);
    
    /**
     * Count total users (for admin purposes)
     */
    @Query("SELECT COUNT(u) FROM User u WHERE u.enabled = true")
    long countActiveUsers();
}
