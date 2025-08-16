package com.anuj.redditmessagemanager.entity;

import jakarta.persistence.*;
import lombok.Data;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;
import org.hibernate.annotations.CreationTimestamp;

import java.time.LocalDateTime;

@Entity
@Table(name = "reddit_messages")
@Data
@NoArgsConstructor
@AllArgsConstructor
public class RedditMessage {
    
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    @Column(name = "reddit_message_id", unique = true, nullable = false)
    private String redditMessageId;
    
    @Column(name = "message_type", nullable = false)
    @Enumerated(EnumType.STRING)
    private MessageType messageType;
    
    @Column(name = "subject", length = 500)
    private String subject;
    
    @Column(name = "body", columnDefinition = "TEXT")
    private String body;
    
    @Column(name = "author")
    private String author;
    
    @Column(name = "recipient")
    private String recipient;
    
    @Column(name = "subreddit")
    private String subreddit;
    
    @Column(name = "is_read")
    private Boolean isRead = false;
    
    @Column(name = "reddit_created_at")
    private LocalDateTime redditCreatedAt;
    
    @Column(name = "context")
    private String context;
    
    @Column(name = "parent_id")
    private String parentId;
    
    @CreationTimestamp
    @Column(name = "stored_at")
    private LocalDateTime storedAt;
    
    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "user_id", nullable = false)
    private User user;
    
    // Enum for message types
    public enum MessageType {
        INBOX,
        SENT,
        UNREAD,
        COMMENT_REPLY,
        POST_REPLY,
        USERNAME_MENTION
    }
    
    // Constructor for creating from Reddit API response
    public RedditMessage(String redditMessageId, MessageType messageType, String subject, 
                        String body, String author, String recipient, User user) {
        this.redditMessageId = redditMessageId;
        this.messageType = messageType;
        this.subject = subject;
        this.body = body;
        this.author = author;
        this.recipient = recipient;
        this.user = user;
        this.isRead = false;
    }
}
