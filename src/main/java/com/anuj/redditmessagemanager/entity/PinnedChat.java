package com.anuj.redditmessagemanager.entity;

import jakarta.persistence.*;
import lombok.Data;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;
import org.hibernate.annotations.CreationTimestamp;

import java.time.LocalDateTime;

@Entity
@Table(name = "pinned_chats",
       uniqueConstraints = @UniqueConstraint(columnNames = {"chat_id", "user_username"}))
@Data
@NoArgsConstructor
@AllArgsConstructor
public class PinnedChat {
    
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "chat_id", nullable = false)
    private Chat chat;
    
    @Column(name = "user_username", nullable = false)
    private String userUsername;
    
    @Column(name = "pin_order")
    private Integer pinOrder = 0;
    
    @Column(name = "is_active")
    private Boolean isActive = true;
    
    @CreationTimestamp
    @Column(name = "pinned_at")
    private LocalDateTime pinnedAt;
    
    @Column(name = "unpinned_at")
    private LocalDateTime unpinnedAt;
    
    // Constructor for creating new pins
    public PinnedChat(Chat chat, String userUsername, Integer pinOrder) {
        this.chat = chat;
        this.userUsername = userUsername;
        this.pinOrder = pinOrder != null ? pinOrder : 0;
        this.isActive = true;
    }
}
