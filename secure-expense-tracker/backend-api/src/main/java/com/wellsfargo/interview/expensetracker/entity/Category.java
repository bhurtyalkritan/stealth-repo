package com.wellsfargo.interview.expensetracker.entity;

import jakarta.persistence.*;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.Size;

/**
 * Category entity for expense categorization
 */
@Entity
@Table(name = "categories", indexes = {
    @Index(name = "idx_user_category", columnList = "user_id, name"),
    @Index(name = "idx_default_category", columnList = "is_default")
})
public class Category {
    
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    @NotBlank(message = "Category name is required")
    @Size(min = 1, max = 100, message = "Category name must be between 1 and 100 characters")
    @Column(nullable = false, length = 100)
    private String name;
    
    @Column(name = "is_default", nullable = false)
    private Boolean isDefault = false;
    
    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "user_id")
    private User user;
    
    // Constructors
    public Category() {}
    
    public Category(String name, Boolean isDefault) {
        this.name = name;
        this.isDefault = isDefault;
    }
    
    public Category(String name, User user) {
        this.name = name;
        this.user = user;
        this.isDefault = false;
    }
    
    // Getters and Setters
    public Long getId() {
        return id;
    }
    
    public void setId(Long id) {
        this.id = id;
    }
    
    public String getName() {
        return name;
    }
    
    public void setName(String name) {
        this.name = name;
    }
    
    public Boolean getIsDefault() {
        return isDefault;
    }
    
    public void setIsDefault(Boolean isDefault) {
        this.isDefault = isDefault;
    }
    
    public User getUser() {
        return user;
    }
    
    public void setUser(User user) {
        this.user = user;
    }
}
