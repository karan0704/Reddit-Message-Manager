package com.anuj.redditmessagemanager.dto;

import com.fasterxml.jackson.annotation.JsonProperty;
import lombok.Data;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;

import java.util.List;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class BulkActionDto {
    
    @JsonProperty("action_type")
    private BulkActionType actionType;
    
    @JsonProperty("chat_ids")
    private List<Long> chatIds;
    
    @JsonProperty("message_ids")
    private List<Long> messageIds;
    
    @JsonProperty("user_ids")
    private List<Long> userIds;
    
    @JsonProperty("usernames")
    private List<String> usernames;
    
    @JsonProperty("reason")
    private String reason; // For blocking users
    
    @JsonProperty("confirm_action")
    private Boolean confirmAction = false;
    
    @JsonProperty("action_metadata")
    private String actionMetadata; // Additional data for specific actions
    
    public enum BulkActionType {
        DELETE_CHATS,
        DELETE_MESSAGES,
        BLOCK_USERS,
        UNBLOCK_USERS,
        PIN_CHATS,
        UNPIN_CHATS,
        MARK_READ,
        MARK_UNREAD,
        EXPORT_CHATS,
        ARCHIVE_CHATS
    }
    
    // Constructor for chat operations
    public BulkActionDto(BulkActionType actionType, List<Long> chatIds) {
        this.actionType = actionType;
        this.chatIds = chatIds;
        this.confirmAction = false;
    }
    
    // Constructor for user operations
    public BulkActionDto(BulkActionType actionType, List<String> usernames, String reason) {
        this.actionType = actionType;
        this.usernames = usernames;
        this.reason = reason;
        this.confirmAction = false;
    }
    
    // Constructor for message operations
    public static BulkActionDto forMessages(BulkActionType actionType, List<Long> messageIds) {
        BulkActionDto dto = new BulkActionDto();
        dto.setActionType(actionType);
        dto.setMessageIds(messageIds);
        dto.setConfirmAction(false);
        return dto;
    }
}
