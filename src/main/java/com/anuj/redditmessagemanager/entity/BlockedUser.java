package com.anuj.redditmessagemanager.entity;

import jakarta.persistence.*;
import lombok.Data;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;
import org.hibernate.annotations.CreationTimestamp;

import java.time.LocalDateTime;

@Entity
@Table(name = "blocked_users", 
       uniqueConstraints = @UniqueConstraint(columnNames = {"blocker_username", "blocked_username"}))
@Data
@NoArgsConstructor
@AllArgsConstructor
public class BlockedUser {
    
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    @Column(name = "blocker_username", nullable = false)
    private String blockerUsername;
    
    @Column(name = "blocked_username", nullable = false)
    private String blockedUsername;
    
    @Column(name = "reason", length = 500)
    private String reason;
    
    @Column(name = "is_active")
    private Boolean isActive = true;
    
    @CreationTimestamp
    @Column(name = "blocked_at")
    private LocalDateTime blockedAt;
    
    @Column(name = "unblocked_at")
    private LocalDateTime unblockedAt;
    
    // Constructor for creating new blocks
    public BlockedUser(String blockerUsername, String blockedUsername, String reason) {
        this.blockerUsername = blockerUsername;
        this.blockedUsername = blockedUsername;
        this.reason = reason;
        this.isActive = true;
    }
}
