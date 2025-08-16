package com.anuj.redditmessagemanager.dto;

import com.anuj.redditmessagemanager.entity.Message.MessageType;
import com.fasterxml.jackson.annotation.JsonProperty;
import lombok.Data;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;

import java.time.LocalDateTime;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class MessageDto {
    
    private Long id;
    
    @JsonProperty("chat_id")
    private Long chatId;
    
    @JsonProperty("sender_username")
    private String senderUsername;
    
    @JsonProperty("message_content")
    private String messageContent;
    
    @JsonProperty("message_type")
    private MessageType messageType;
    
    @JsonProperty("image_url")
    private String imageUrl;
    
    @JsonProperty("is_read")
    private Boolean isRead;
    
    @JsonProperty("is_deleted")
    private Boolean isDeleted;
    
    @JsonProperty("is_image_hidden")
    private Boolean isImageHidden;
    
    @JsonProperty("created_at")
    private LocalDateTime createdAt;
    
    @JsonProperty("is_own_message")
    private Boolean isOwnMessage; // Helper field for UI
    
    @JsonProperty("formatted_time")
    private String formattedTime; // Helper field for display
    
    @JsonProperty("is_selected")
    private Boolean isSelected = false; // For bulk operations
    
    // Constructor for sending new messages
    public MessageDto(String messageContent, MessageType messageType) {
        this.messageContent = messageContent;
        this.messageType = messageType != null ? messageType : MessageType.TEXT;
        this.isRead = false;
        this.isDeleted = false;
        this.isImageHidden = true;
    }
    
    // Constructor for API responses
    public MessageDto(Long id, String senderUsername, String messageContent, 
                     MessageType messageType, LocalDateTime createdAt, Boolean isRead) {
        this.id = id;
        this.senderUsername = senderUsername;
        this.messageContent = messageContent;
        this.messageType = messageType;
        this.createdAt = createdAt;
        this.isRead = isRead != null ? isRead : false;
        this.isDeleted = false;
    }
}
