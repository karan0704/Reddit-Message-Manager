package com.anuj.redditmessagemanager.entity;

import jakarta.persistence.*;
import lombok.Data;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;
import org.hibernate.annotations.CreationTimestamp;

import java.time.LocalDateTime;

@Entity
@Table(name = "messages")
@Data
@NoArgsConstructor
@AllArgsConstructor
public class Message {
    
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "chat_id", nullable = false)
    private Chat chat;
    
    @Column(name = "sender_username", nullable = false)
    private String senderUsername;
    
    @Column(name = "message_content", columnDefinition = "TEXT")
    private String messageContent;
    
    @Column(name = "message_type")
    @Enumerated(EnumType.STRING)
    private MessageType messageType = MessageType.TEXT;
    
    @Column(name = "image_url")
    private String imageUrl;
    
    @Column(name = "file_url")
    private String fileUrl;
    
    @Column(name = "file_name")
    private String fileName;
    
    @Column(name = "file_size")
    private Long fileSize;
    
    @Column(name = "is_read")
    private Boolean isRead = false;
    
    @Column(name = "is_deleted")
    private Boolean isDeleted = false;
    
    @Column(name = "is_image_hidden")
    private Boolean isImageHidden = true;
    
    @Column(name = "reply_to_message_id")
    private Long replyToMessageId;
    
    @CreationTimestamp
    @Column(name = "created_at")
    private LocalDateTime createdAt;
    
    @Column(name = "edited_at")
    private LocalDateTime editedAt;
    
    public enum MessageType {
        TEXT, IMAGE, FILE, SYSTEM
    }
    
    // Constructor for creating new messages
    public Message(Chat chat, String senderUsername, String messageContent, MessageType messageType) {
        this.chat = chat;
        this.senderUsername = senderUsername;
        this.messageContent = messageContent;
        this.messageType = messageType != null ? messageType : MessageType.TEXT;
        this.isRead = false;
        this.isDeleted = false;
        this.isImageHidden = messageType == MessageType.IMAGE;
    }
}
