package com.anuj.redditmessagemanager.dto;

import com.fasterxml.jackson.annotation.JsonProperty;
import lombok.Data;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;

import java.time.LocalDateTime;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class BlockedUserDto {
    
    private Long id;
    
    @JsonProperty("blocker_username")
    private String blockerUsername;
    
    @JsonProperty("blocked_username")
    private String blockedUsername;
    
    @JsonProperty("blocked_user_display_name")
    private String blockedUserDisplayName;
    
    private String reason;
    
    @JsonProperty("blocked_at")
    private LocalDateTime blockedAt;
    
    @JsonProperty("is_selected")
    private Boolean isSelected = false; // For bulk operations
    
    @JsonProperty("can_unblock")
    private Boolean canUnblock = true;
    
    @JsonProperty("blocked_user_avatar")
    private String blockedUserAvatar;
    
    @JsonProperty("formatted_blocked_time")
    private String formattedBlockedTime;
    
    // Constructor for API responses
    public BlockedUserDto(String blockerUsername, String blockedUsername, String reason, LocalDateTime blockedAt) {
        this.blockerUsername = blockerUsername;
        this.blockedUsername = blockedUsername;
        this.reason = reason;
        this.blockedAt = blockedAt;
        this.isSelected = false;
        this.canUnblock = true;
    }
    
    // Constructor for creating block requests
    public BlockedUserDto(String blockedUsername, String reason) {
        this.blockedUsername = blockedUsername;
        this.reason = reason;
    }
}
