import os

def create_all_dto_classes():
    # Base path from your previous conversation
    base_path = "D:\\Karan Ticket Project\\Reddit Message Manager"

    # DTO classes for the local chat application
    dto_files = [
        {
            "path": "src\\main\\java\\com\\anuj\\redditmessagemanager\\dto\\ChatDto.java",
            "content": """package com.anuj.redditmessagemanager.dto;

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
"""
        },

        {
            "path": "src\\main\\java\\com\\anuj\\redditmessagemanager\\dto\\MessageDto.java",
            "content": """package com.anuj.redditmessagemanager.dto;

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
"""
        },

        {
            "path": "src\\main\\java\\com\\anuj\\redditmessagemanager\\dto\\UserDto.java",
            "content": """package com.anuj.redditmessagemanager.dto;

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
"""
        },

        {
            "path": "src\\main\\java\\com\\anuj\\redditmessagemanager\\dto\\SearchResultDto.java",
            "content": """package com.anuj.redditmessagemanager.dto;

import com.anuj.redditmessagemanager.entity.SearchHistory.SearchType;
import com.fasterxml.jackson.annotation.JsonProperty;
import lombok.Data;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;

import java.util.List;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class SearchResultDto {
    
    @JsonProperty("search_query")
    private String searchQuery;
    
    @JsonProperty("search_type")
    private SearchType searchType;
    
    @JsonProperty("total_results")
    private Integer totalResults;
    
    @JsonProperty("page")
    private Integer page;
    
    @JsonProperty("page_size")
    private Integer pageSize;
    
    @JsonProperty("has_more")
    private Boolean hasMore;
    
    // Different result types
    private List<MessageDto> messages;
    private List<ChatDto> chats;
    private List<UserDto> users;
    
    @JsonProperty("search_time_ms")
    private Long searchTimeMs;
    
    @JsonProperty("highlighted_terms")
    private List<String> highlightedTerms;
    
    @JsonProperty("suggestions")
    private List<String> suggestions;
    
    // Constructor for message search results
    public SearchResultDto(String searchQuery, List<MessageDto> messages, Integer totalResults) {
        this.searchQuery = searchQuery;
        this.searchType = SearchType.MESSAGES;
        this.messages = messages;
        this.totalResults = totalResults;
        this.page = 0;
        this.pageSize = messages != null ? messages.size() : 0;
        this.hasMore = false;
    }
    
    // Constructor for user search results
    public SearchResultDto(String searchQuery, List<UserDto> users) {
        this.searchQuery = searchQuery;
        this.searchType = SearchType.USERS;
        this.users = users;
        this.totalResults = users != null ? users.size() : 0;
    }
    
    // Constructor for chat search results
    public SearchResultDto(String searchQuery, List<ChatDto> chats) {
        this.searchQuery = searchQuery;
        this.searchType = SearchType.POSTS; // Reusing existing enum value
        this.chats = chats;
        this.totalResults = chats != null ? chats.size() : 0;
    }
}
"""
        },

        {
            "path": "src\\main\\java\\com\\anuj\\redditmessagemanager\\dto\\FilterDto.java",
            "content": """package com.anuj.redditmessagemanager.dto;

import com.fasterxml.jackson.annotation.JsonProperty;
import lombok.Data;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;

import java.time.LocalDateTime;
import java.util.List;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class FilterDto {
    
    @JsonProperty("date_from")
    private LocalDateTime dateFrom;
    
    @JsonProperty("date_to")
    private LocalDateTime dateTo;
    
    @JsonProperty("username_filter")
    private String usernameFilter;
    
    @JsonProperty("username_starts_with")
    private String usernameStartsWith;
    
    @JsonProperty("username_contains")
    private String usernameContains;
    
    @JsonProperty("message_content_filter")
    private String messageContentFilter;
    
    @JsonProperty("only_pinned")
    private Boolean onlyPinned;
    
    @JsonProperty("only_unread")
    private Boolean onlyUnread;
    
    @JsonProperty("only_with_images")
    private Boolean onlyWithImages;
    
    @JsonProperty("exclude_blocked")
    private Boolean excludeBlocked;
    
    @JsonProperty("chat_ids")
    private List<Long> chatIds; // For specific chat filtering
    
    @JsonProperty("user_ids")
    private List<Long> userIds; // For specific user filtering
    
    @JsonProperty("sort_by")
    private String sortBy; // "recent", "oldest", "username", "message_count"
    
    @JsonProperty("sort_direction")
    private String sortDirection; // "asc", "desc"
    
    @JsonProperty("page")
    private Integer page = 0;
    
    @JsonProperty("page_size")
    private Integer pageSize = 20;
    
    // Constructor for date range filtering
    public FilterDto(LocalDateTime dateFrom, LocalDateTime dateTo) {
        this.dateFrom = dateFrom;
        this.dateTo = dateTo;
        this.onlyPinned = false;
        this.onlyUnread = false;
        this.excludeBlocked = true;
        this.sortBy = "recent";
        this.sortDirection = "desc";
    }
    
    // Constructor for username filtering
    public FilterDto(String usernameFilter, Boolean onlyUnread) {
        this.usernameFilter = usernameFilter;
        this.onlyUnread = onlyUnread;
        this.excludeBlocked = true;
        this.sortBy = "recent";
        this.sortDirection = "desc";
    }
}
"""
        },

        {
            "path": "src\\main\\java\\com\\anuj\\redditmessagemanager\\dto\\BulkActionDto.java",
            "content": """package com.anuj.redditmessagemanager.dto;

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
"""
        },

        {
            "path": "src\\main\\java\\com\\anuj\\redditmessagemanager\\dto\\ExportDto.java",
            "content": """package com.anuj.redditmessagemanager.dto;

import com.fasterxml.jackson.annotation.JsonProperty;
import lombok.Data;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;

import java.time.LocalDateTime;
import java.util.List;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class ExportDto {
    
    @JsonProperty("export_format")
    private ExportFormat exportFormat;
    
    @JsonProperty("chat_ids")
    private List<Long> chatIds;
    
    @JsonProperty("date_from")
    private LocalDateTime dateFrom;
    
    @JsonProperty("date_to")
    private LocalDateTime dateTo;
    
    @JsonProperty("include_images")
    private Boolean includeImages;
    
    @JsonProperty("include_metadata")
    private Boolean includeMetadata;
    
    @JsonProperty("max_messages")
    private Integer maxMessages;
    
    @JsonProperty("filename")
    private String filename;
    
    @JsonProperty("export_size_mb")
    private Double exportSizeMb;
    
    @JsonProperty("message_count")
    private Integer messageCount;
    
    @JsonProperty("download_url")
    private String downloadUrl;
    
    @JsonProperty("export_status")
    private ExportStatus exportStatus;
    
    @JsonProperty("created_at")
    private LocalDateTime createdAt;
    
    @JsonProperty("completed_at")
    private LocalDateTime completedAt;
    
    @JsonProperty("error_message")
    private String errorMessage;
    
    public enum ExportFormat {
        TXT, JSON, CSV, HTML, PDF
    }
    
    public enum ExportStatus {
        PENDING, IN_PROGRESS, COMPLETED, FAILED, EXPIRED
    }
    
    // Constructor for export request
    public ExportDto(ExportFormat exportFormat, List<Long> chatIds, LocalDateTime dateFrom, 
                    LocalDateTime dateTo, Boolean includeImages) {
        this.exportFormat = exportFormat;
        this.chatIds = chatIds;
        this.dateFrom = dateFrom;
        this.dateTo = dateTo;
        this.includeImages = includeImages != null ? includeImages : false;
        this.includeMetadata = true;
        this.maxMessages = 10000;
        this.exportStatus = ExportStatus.PENDING;
        this.createdAt = LocalDateTime.now();
    }
    
    // Constructor for export response
    public ExportDto(String filename, Double exportSizeMb, Integer messageCount, 
                    String downloadUrl, ExportStatus status) {
        this.filename = filename;
        this.exportSizeMb = exportSizeMb;
        this.messageCount = messageCount;
        this.downloadUrl = downloadUrl;
        this.exportStatus = status;
    }
}
"""
        },

        {
            "path": "src\\main\\java\\com\\anuj\\redditmessagemanager\\dto\\BlockedUserDto.java",
            "content": """package com.anuj.redditmessagemanager.dto;

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
"""
        },

        {
            "path": "src\\main\\java\\com\\anuj\\redditmessagemanager\\dto\\PinnedChatDto.java",
            "content": """package com.anuj.redditmessagemanager.dto;

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
"""
        },

        {
            "path": "src\\main\\java\\com\\anuj\\redditmessagemanager\\dto\\AuthDto.java",
            "content": """package com.anuj.redditmessagemanager.dto;

import com.fasterxml.jackson.annotation.JsonProperty;
import lombok.Data;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;

import java.time.LocalDateTime;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class AuthDto {
    
    private String username;
    
    private String password;
    
    @JsonProperty("display_name")
    private String displayName;
    
    private String email;
    
    @JsonProperty("remember_me")
    private Boolean rememberMe;
    
    @JsonProperty("is_authenticated")
    private Boolean isAuthenticated;
    
    @JsonProperty("session_token")
    private String sessionToken;
    
    @JsonProperty("login_time")
    private LocalDateTime loginTime;
    
    @JsonProperty("last_activity")
    private LocalDateTime lastActivity;
    
    @JsonProperty("user_agent")
    private String userAgent;
    
    @JsonProperty("ip_address")
    private String ipAddress;
    
    @JsonProperty("is_remembered_user")
    private Boolean isRememberedUser = false;
    
    @JsonProperty("previous_login")
    private LocalDateTime previousLogin;
    
    // Constructor for login requests
    public AuthDto(String username, String password, Boolean rememberMe) {
        this.username = username;
        this.password = password;
        this.rememberMe = rememberMe != null ? rememberMe : false;
    }
    
    // Constructor for authentication responses
    public AuthDto(String username, String displayName, Boolean isAuthenticated, String sessionToken) {
        this.username = username;
        this.displayName = displayName;
        this.isAuthenticated = isAuthenticated;
        this.sessionToken = sessionToken;
        this.loginTime = LocalDateTime.now();
    }
    
    // Constructor for remembered user
    public static AuthDto createRememberedUser(String username, String displayName, LocalDateTime previousLogin) {
        AuthDto auth = new AuthDto();
        auth.setUsername(username);
        auth.setDisplayName(displayName);
        auth.setIsRememberedUser(true);
        auth.setPreviousLogin(previousLogin);
        auth.setRememberMe(true);
        return auth;
    }
}
"""
        }
    ]

    # Function to create files
    def create_files(files_list, file_type):
        print(f"\nCreating {file_type} files...")

        for file_info in files_list:
            full_file_path = os.path.join(base_path, file_info["path"])

            try:
                # Create directory if it doesn't exist
                os.makedirs(os.path.dirname(full_file_path), exist_ok=True)

                # Create file (overwrite if exists)
                with open(full_file_path, 'w', encoding='utf-8') as f:
                    f.write(file_info["content"])
                print(f"✓ Created: {file_info['path']}")

            except Exception as e:
                print(f"✗ Failed to create {file_info['path']}: {str(e)}")

    # Create all DTO files
    create_files(dto_files, "DTO")

    print("\n" + "="*70)
    print("All DTO classes created successfully!")
    print("="*70)

    print("\nCreated DTO Classes:")
    print("✓ ChatDto.java - Chat conversation data transfer")
    print("✓ MessageDto.java - Individual message data transfer")
    print("✓ UserDto.java - User profile and status information")
    print("✓ SearchResultDto.java - Search results with pagination")
    print("✓ FilterDto.java - Advanced filtering options")
    print("✓ BulkActionDto.java - Bulk operations (delete, block, etc.)")
    print("✓ ExportDto.java - Chat export functionality")
    print("✓ BlockedUserDto.java - Blocked user management")
    print("✓ PinnedChatDto.java - Pinned chat management")
    print("✓ AuthDto.java - Local authentication data")

    print("\nDTO Features included:")
    print("• JSON property mapping with snake_case")
    print("• Lombok annotations for clean code")
    print("• Multiple constructors for different use cases")
    print("• Helper fields for UI operations")
    print("• Bulk operation support")
    print("• Pagination support")
    print("• Export functionality")
    print("• Local authentication")
    print("• Chat management features")
    print("• User blocking/unblocking")
    print("• Pin/unpin functionality")
    print("• Image handling")
    print("• Search and filtering")

    print("\nNext steps:")
    print("1. Update your repositories to work with these DTOs")
    print("2. Update your services to convert entities to DTOs")
    print("3. Update your controllers to use these DTOs")
    print("4. Test the API endpoints with the new DTO structure")

if __name__ == "__main__":
    create_all_dto_classes()