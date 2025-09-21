package com.wellsfargo.interview.expensetracker.repository;

import com.wellsfargo.interview.expensetracker.entity.Category;
import com.wellsfargo.interview.expensetracker.entity.User;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.util.List;
import java.util.Optional;

/**
 * Repository interface for Category entity operations
 */
@Repository
public interface CategoryRepository extends JpaRepository<Category, Long> {
    
    /**
     * Find all default categories
     */
    List<Category> findByIsDefaultTrue();
    
    /**
     * Find categories by user (including default categories)
     */
    @Query("SELECT c FROM Category c WHERE c.isDefault = true OR c.user = :user ORDER BY c.isDefault DESC, c.name ASC")
    List<Category> findAvailableCategoriesForUser(@Param("user") User user);
    
    /**
     * Find user-specific categories only
     */
    List<Category> findByUserAndIsDefaultFalse(User user);
    
    /**
     * Check if category name exists for user (including defaults)
     */
    @Query("SELECT c FROM Category c WHERE LOWER(c.name) = LOWER(:name) AND (c.isDefault = true OR c.user = :user)")
    Optional<Category> findByNameAndUserOrDefault(@Param("name") String name, @Param("user") User user);
    
    /**
     * Find category by name and user
     */
    Optional<Category> findByNameIgnoreCaseAndUser(String name, User user);
    
    /**
     * Get category usage statistics
     */
    @Query("SELECT c.name, COUNT(t) FROM Category c LEFT JOIN Transaction t ON c.name = t.category AND t.user = :user " +
           "WHERE c.isDefault = true OR c.user = :user " +
           "GROUP BY c.name ORDER BY COUNT(t) DESC")
    List<Object[]> getCategoryUsageStats(@Param("user") User user);
}
