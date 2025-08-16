package com.anuj.redditmessagemanager.entity;

import jakarta.persistence.*;
import lombok.Data;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;
import org.hibernate.annotations.CreationTimestamp;

import java.time.LocalDateTime;

@Entity
@Table(name = "unread_messages",
       uniqueConstraints = @UniqueConstraint(columnNames = {"message_id", "user_username"}))
@Data
@NoArgsConstructor
@AllArgsConstructor
public class UnreadMessage {
    
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "message_id", nullable = false)
    private Message message;
    
    @Column(name = "user_username", nullable = false)
    private String userUsername;
    
    @Column(name = "is_notification_sent")
    private Boolean isNotificationSent = false;
    
    @CreationTimestamp
    @Column(name = "created_at")
    private LocalDateTime createdAt;
    
    @Column(name = "read_at")
    private LocalDateTime readAt;
    
    // Constructor for creating unread message tracking
    public UnreadMessage(Message message, String userUsername) {
        this.message = message;
        this.userUsername = userUsername;
        this.isNotificationSent = false;
    }
}
