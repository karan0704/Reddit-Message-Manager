package com.anuj.redditmessagemanager.dto;

import com.fasterxml.jackson.annotation.JsonProperty;
import lombok.Data;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;

import java.time.LocalDateTime;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class UserDto {
    
    private Long id;
    
    private String username;
    
    @JsonProperty("display_name")
    private String displayName;
    
    private String email;
    
    @JsonProperty("is_active")
    private Boolean isActive;
    
    @JsonProperty("is_online")
    private Boolean isOnline;
    
    @JsonProperty("last_seen")
    private LocalDateTime lastSeen;
    
    @JsonProperty("created_at")
    private LocalDateTime createdAt;
    
    @JsonProperty("avatar_url")
    private String avatarUrl;
    
    @JsonProperty("chat_count")
    private Long chatCount;
    
    @JsonProperty("message_count")
    private Long messageCount;
    
    @JsonProperty("unread_count")
    private Long unreadCount;
    
    @JsonProperty("is_blocked")
    private Boolean isBlocked = false;
    
    @JsonProperty("is_remembered")
    private Boolean isRemembered = false; // For "remember last user" feature
    
    // Constructor without sensitive data
    public UserDto(String username, String displayName, Boolean isActive, LocalDateTime createdAt) {
        this.username = username;
        this.displayName = displayName;
        this.isActive = isActive;
        this.createdAt = createdAt;
        this.isOnline = false;
        this.isBlocked = false;
    }
    
    // Constructor for autocomplete suggestions
    public UserDto(String username, String displayName, String avatarUrl) {
        this.username = username;
        this.displayName = displayName;
        this.avatarUrl = avatarUrl;
    }
}
