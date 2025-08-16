package com.anuj.redditmessagemanager.dto;

import com.anuj.redditmessagemanager.entity.RedditMessage.MessageType;
import com.fasterxml.jackson.annotation.JsonProperty;
import lombok.Data;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;

import java.time.LocalDateTime;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class RedditMessageDto {
    
    private Long id;
    
    @JsonProperty("reddit_message_id")
    private String redditMessageId;
    
    @JsonProperty("message_type")
    private MessageType messageType;
    
    private String subject;
    private String body;
    private String author;
    private String recipient;
    private String subreddit;
    
    @JsonProperty("is_read")
    private Boolean isRead;
    
    @JsonProperty("reddit_created_at")
    private LocalDateTime redditCreatedAt;
    
    private String context;
    
    @JsonProperty("parent_id")
    private String parentId;
    
    @JsonProperty("stored_at")
    private LocalDateTime storedAt;
    
    // Constructor for API responses
    public RedditMessageDto(String subject, String body, String author, MessageType messageType) {
        this.subject = subject;
        this.body = body;
        this.author = author;
        this.messageType = messageType;
        this.isRead = false;
    }
}
