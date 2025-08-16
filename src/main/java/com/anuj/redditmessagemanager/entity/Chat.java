package com.anuj.redditmessagemanager.entity;

import jakarta.persistence.*;
import lombok.Data;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;
import org.hibernate.annotations.CreationTimestamp;
import org.hibernate.annotations.UpdateTimestamp;

import java.time.LocalDateTime;
import java.util.List;

@Entity
@Table(name = "chats")
@Data
@NoArgsConstructor
@AllArgsConstructor
public class Chat {
    
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    @Column(name = "user1_username", nullable = false)
    private String user1Username;
    
    @Column(name = "user2_username", nullable = false)
    private String user2Username;
    
    @Column(name = "last_message", length = 500)
    private String lastMessage;
    
    @Column(name = "last_message_timestamp")
    private LocalDateTime lastMessageTimestamp;
    
    @Column(name = "is_pinned")
    private Boolean isPinned = false;
    
    @Column(name = "has_unread")
    private Boolean hasUnread = false;
    
    @Column(name = "unread_count")
    private Integer unreadCount = 0;
    
    @Column(name = "is_archived")
    private Boolean isArchived = false;
    
    @CreationTimestamp
    @Column(name = "created_at")
    private LocalDateTime createdAt;
    
    @UpdateTimestamp
    @Column(name = "updated_at")
    private LocalDateTime updatedAt;
    
    @OneToMany(mappedBy = "chat", cascade = CascadeType.ALL, fetch = FetchType.LAZY)
    private List<Message> messages;
    
    @OneToMany(mappedBy = "chat", cascade = CascadeType.ALL, fetch = FetchType.LAZY)
    private List<PinnedChat> pinnedChats;
    
    // Constructor for creating new chats
    public Chat(String user1Username, String user2Username) {
        this.user1Username = user1Username;
        this.user2Username = user2Username;
        this.lastMessageTimestamp = LocalDateTime.now();
        this.isPinned = false;
        this.hasUnread = false;
        this.unreadCount = 0;
        this.isArchived = false;
    }
}
