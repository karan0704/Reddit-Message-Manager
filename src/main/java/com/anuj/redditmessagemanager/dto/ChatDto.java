package com.anuj.redditmessagemanager.dto;

import com.fasterxml.jackson.annotation.JsonProperty;
import lombok.Data;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;

import java.time.LocalDateTime;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class ChatDto {
    
    private Long id;
    
    @JsonProperty("user1_username")
    private String user1Username;
    
    @JsonProperty("user2_username")
    private String user2Username;
    
    @JsonProperty("other_username")
    private String otherUsername; // The other participant from current user's perspective
    
    @JsonProperty("last_message")
    private String lastMessage;
    
    @JsonProperty("last_message_timestamp")
    private LocalDateTime lastMessageTimestamp;
    
    @JsonProperty("is_pinned")
    private Boolean isPinned;
    
    @JsonProperty("has_unread")
    private Boolean hasUnread;
    
    @JsonProperty("unread_count")
    private Integer unreadCount;
    
    @JsonProperty("created_at")
    private LocalDateTime createdAt;
    
    @JsonProperty("updated_at")
    private LocalDateTime updatedAt;
    
    @JsonProperty("is_selected")
    private Boolean isSelected = false; // For bulk operations
    
    @JsonProperty("is_blocked")
    private Boolean isBlocked = false;
    
    // Constructor for creating from entities
    public ChatDto(Long id, String user1Username, String user2Username, String lastMessage,
                   LocalDateTime lastMessageTimestamp, Boolean isPinned, Boolean hasUnread, 
                   Integer unreadCount) {
        this.id = id;
        this.user1Username = user1Username;
        this.user2Username = user2Username;
        this.lastMessage = lastMessage;
        this.lastMessageTimestamp = lastMessageTimestamp;
        this.isPinned = isPinned != null ? isPinned : false;
        this.hasUnread = hasUnread != null ? hasUnread : false;
        this.unreadCount = unreadCount != null ? unreadCount : 0;
    }
}
