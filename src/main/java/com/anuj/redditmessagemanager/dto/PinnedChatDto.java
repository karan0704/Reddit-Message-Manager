package com.anuj.redditmessagemanager.dto;

import com.fasterxml.jackson.annotation.JsonProperty;
import lombok.Data;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;

import java.time.LocalDateTime;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class PinnedChatDto {
    
    private Long id;
    
    @JsonProperty("chat_id")
    private Long chatId;
    
    @JsonProperty("user_username")
    private String userUsername;
    
    @JsonProperty("pinned_at")
    private LocalDateTime pinnedAt;
    
    @JsonProperty("pin_order")
    private Integer pinOrder; // For custom ordering of pinned chats
    
    @JsonProperty("chat_info")
    private ChatDto chatInfo; // Embedded chat information
    
    @JsonProperty("is_active")
    private Boolean isActive = true;
    
    // Constructor for creating pin requests
    public PinnedChatDto(Long chatId, String userUsername) {
        this.chatId = chatId;
        this.userUsername = userUsername;
        this.pinnedAt = LocalDateTime.now();
        this.isActive = true;
        this.pinOrder = 0;
    }
    
    // Constructor with pin order
    public PinnedChatDto(Long chatId, String userUsername, Integer pinOrder) {
        this.chatId = chatId;
        this.userUsername = userUsername;
        this.pinnedAt = LocalDateTime.now();
        this.pinOrder = pinOrder;
        this.isActive = true;
    }
}
