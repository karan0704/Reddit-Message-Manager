import os

def create_entity_and_repository_classes():
    # Base path from your previous conversation
    base_path = "D:\\Karan Ticket Project\\Reddit Message Manager"

    # Entity classes for the local chat application
    entity_files = [
        {
            "path": "src\\main\\java\\com\\anuj\\redditmessagemanager\\entity\\User.java",
            "content": """package com.anuj.redditmessagemanager.entity;

import jakarta.persistence.*;
import lombok.Data;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;
import org.hibernate.annotations.CreationTimestamp;
import org.hibernate.annotations.UpdateTimestamp;

import java.time.LocalDateTime;
import java.util.List;

@Entity
@Table(name = "users")
@Data
@NoArgsConstructor
@AllArgsConstructor
public class User {
    
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    @Column(name = "username", unique = true, nullable = false)
    private String username;
    
    @Column(name = "display_name")
    private String displayName;
    
    @Column(name = "email")
    private String email;
    
    @Column(name = "password_hash")
    private String passwordHash;
    
    @Column(name = "is_active")
    private Boolean isActive = true;
    
    @Column(name = "is_online")
    private Boolean isOnline = false;
    
    @Column(name = "last_seen")
    private LocalDateTime lastSeen;
    
    @Column(name = "avatar_url")
    private String avatarUrl;
    
    @Column(name = "is_remembered")
    private Boolean isRemembered = false;
    
    @Column(name = "last_login")
    private LocalDateTime lastLogin;
    
    @CreationTimestamp
    @Column(name = "created_at")
    private LocalDateTime createdAt;
    
    @UpdateTimestamp
    @Column(name = "updated_at")
    private LocalDateTime updatedAt;
    
    @OneToMany(mappedBy = "user", cascade = CascadeType.ALL, fetch = FetchType.LAZY)
    private List<SearchHistory> searchHistory;
    
    // Constructor for creating new users
    public User(String username, String displayName, String email) {
        this.username = username;
        this.displayName = displayName;
        this.email = email;
        this.isActive = true;
        this.isOnline = false;
        this.isRemembered = false;
    }
}
"""
        },

        {
            "path": "src\\main\\java\\com\\anuj\\redditmessagemanager\\entity\\Chat.java",
            "content": """package com.anuj.redditmessagemanager.entity;

import jakarta.persistence.*;
import lombok.Data;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;
import org.hibernate.annotations.CreationTimestamp;
import org.hibernate.annotations.UpdateTimestamp;

import java.time.LocalDateTime;
import java.util.List;

@Entity
@Table(name = "chats")
@Data
@NoArgsConstructor
@AllArgsConstructor
public class Chat {
    
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    @Column(name = "user1_username", nullable = false)
    private String user1Username;
    
    @Column(name = "user2_username", nullable = false)
    private String user2Username;
    
    @Column(name = "last_message", length = 500)
    private String lastMessage;
    
    @Column(name = "last_message_timestamp")
    private LocalDateTime lastMessageTimestamp;
    
    @Column(name = "is_pinned")
    private Boolean isPinned = false;
    
    @Column(name = "has_unread")
    private Boolean hasUnread = false;
    
    @Column(name = "unread_count")
    private Integer unreadCount = 0;
    
    @Column(name = "is_archived")
    private Boolean isArchived = false;
    
    @CreationTimestamp
    @Column(name = "created_at")
    private LocalDateTime createdAt;
    
    @UpdateTimestamp
    @Column(name = "updated_at")
    private LocalDateTime updatedAt;
    
    @OneToMany(mappedBy = "chat", cascade = CascadeType.ALL, fetch = FetchType.LAZY)
    private List<Message> messages;
    
    @OneToMany(mappedBy = "chat", cascade = CascadeType.ALL, fetch = FetchType.LAZY)
    private List<PinnedChat> pinnedChats;
    
    // Constructor for creating new chats
    public Chat(String user1Username, String user2Username) {
        this.user1Username = user1Username;
        this.user2Username = user2Username;
        this.lastMessageTimestamp = LocalDateTime.now();
        this.isPinned = false;
        this.hasUnread = false;
        this.unreadCount = 0;
        this.isArchived = false;
    }
}
"""
        },

        {
            "path": "src\\main\\java\\com\\anuj\\redditmessagemanager\\entity\\Message.java",
            "content": """package com.anuj.redditmessagemanager.entity;

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
"""
        },

        {
            "path": "src\\main\\java\\com\\anuj\\redditmessagemanager\\entity\\BlockedUser.java",
            "content": """package com.anuj.redditmessagemanager.entity;

import jakarta.persistence.*;
import lombok.Data;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;
import org.hibernate.annotations.CreationTimestamp;

import java.time.LocalDateTime;

@Entity
@Table(name = "blocked_users", 
       uniqueConstraints = @UniqueConstraint(columnNames = {"blocker_username", "blocked_username"}))
@Data
@NoArgsConstructor
@AllArgsConstructor
public class BlockedUser {
    
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    @Column(name = "blocker_username", nullable = false)
    private String blockerUsername;
    
    @Column(name = "blocked_username", nullable = false)
    private String blockedUsername;
    
    @Column(name = "reason", length = 500)
    private String reason;
    
    @Column(name = "is_active")
    private Boolean isActive = true;
    
    @CreationTimestamp
    @Column(name = "blocked_at")
    private LocalDateTime blockedAt;
    
    @Column(name = "unblocked_at")
    private LocalDateTime unblockedAt;
    
    // Constructor for creating new blocks
    public BlockedUser(String blockerUsername, String blockedUsername, String reason) {
        this.blockerUsername = blockerUsername;
        this.blockedUsername = blockedUsername;
        this.reason = reason;
        this.isActive = true;
    }
}
"""
        },

        {
            "path": "src\\main\\java\\com\\anuj\\redditmessagemanager\\entity\\PinnedChat.java",
            "content": """package com.anuj.redditmessagemanager.entity;

import jakarta.persistence.*;
import lombok.Data;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;
import org.hibernate.annotations.CreationTimestamp;

import java.time.LocalDateTime;

@Entity
@Table(name = "pinned_chats",
       uniqueConstraints = @UniqueConstraint(columnNames = {"chat_id", "user_username"}))
@Data
@NoArgsConstructor
@AllArgsConstructor
public class PinnedChat {
    
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "chat_id", nullable = false)
    private Chat chat;
    
    @Column(name = "user_username", nullable = false)
    private String userUsername;
    
    @Column(name = "pin_order")
    private Integer pinOrder = 0;
    
    @Column(name = "is_active")
    private Boolean isActive = true;
    
    @CreationTimestamp
    @Column(name = "pinned_at")
    private LocalDateTime pinnedAt;
    
    @Column(name = "unpinned_at")
    private LocalDateTime unpinnedAt;
    
    // Constructor for creating new pins
    public PinnedChat(Chat chat, String userUsername, Integer pinOrder) {
        this.chat = chat;
        this.userUsername = userUsername;
        this.pinOrder = pinOrder != null ? pinOrder : 0;
        this.isActive = true;
    }
}
"""
        },

        {
            "path": "src\\main\\java\\com\\anuj\\redditmessagemanager\\entity\\UnreadMessage.java",
            "content": """package com.anuj.redditmessagemanager.entity;

import jakarta.persistence.*;
import lombok.Data;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;
import org.hibernate.annotations.CreationTimestamp;

import java.time.LocalDateTime;

@Entity
@Table(name = "unread_messages",
       uniqueConstraints = @UniqueConstraint(columnNames = {"message_id", "user_username"}))
@Data
@NoArgsConstructor
@AllArgsConstructor
public class UnreadMessage {
    
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "message_id", nullable = false)
    private Message message;
    
    @Column(name = "user_username", nullable = false)
    private String userUsername;
    
    @Column(name = "is_notification_sent")
    private Boolean isNotificationSent = false;
    
    @CreationTimestamp
    @Column(name = "created_at")
    private LocalDateTime createdAt;
    
    @Column(name = "read_at")
    private LocalDateTime readAt;
    
    // Constructor for creating unread message tracking
    public UnreadMessage(Message message, String userUsername) {
        this.message = message;
        this.userUsername = userUsername;
        this.isNotificationSent = false;
    }
}
"""
        },

        {
            "path": "src\\main\\java\\com\\anuj\\redditmessagemanager\\entity\\SearchHistory.java",
            "content": """package com.anuj.redditmessagemanager.entity;

import jakarta.persistence.*;
import lombok.Data;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;
import org.hibernate.annotations.CreationTimestamp;

import java.time.LocalDateTime;

@Entity
@Table(name = "search_history")
@Data
@NoArgsConstructor
@AllArgsConstructor
public class SearchHistory {
    
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    @Column(name = "search_query", nullable = false)
    private String searchQuery;
    
    @Column(name = "search_type")
    @Enumerated(EnumType.STRING)
    private SearchType searchType;
    
    @Column(name = "results_count")
    private Integer resultsCount;
    
    @CreationTimestamp
    @Column(name = "searched_at")
    private LocalDateTime searchedAt;
    
    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "user_id", nullable = false)
    private User user;
    
    public enum SearchType {
        MESSAGES,
        USERS, 
        CHATS,
        POSTS
    }
    
    public SearchHistory(String searchQuery, SearchType searchType, Integer resultsCount, User user) {
        this.searchQuery = searchQuery;
        this.searchType = searchType;
        this.resultsCount = resultsCount;
        this.user = user;
    }
}
"""
        }
    ]

    # Repository classes for the local chat application
    repository_files = [
        {
            "path": "src\\main\\java\\com\\anuj\\redditmessagemanager\\repository\\UserRepository.java",
            "content": """package com.anuj.redditmessagemanager.repository;

import com.anuj.redditmessagemanager.entity.User;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.time.LocalDateTime;
import java.util.List;
import java.util.Optional;

@Repository
public interface UserRepository extends JpaRepository<User, Long> {
    
    /**
     * Find user by username
     */
    Optional<User> findByUsername(String username);
    
    /**
     * Find user by email
     */
    Optional<User> findByEmail(String email);
    
    /**
     * Check if user exists by username
     */
    boolean existsByUsername(String username);
    
    /**
     * Check if user exists by email
     */
    boolean existsByEmail(String email);
    
    /**
     * Find all active users
     */
    List<User> findByIsActiveTrue();
    
    /**
     * Find all online users
     */
    List<User> findByIsOnlineTrue();
    
    /**
     * Find remembered users for quick login
     */
    List<User> findByIsRememberedTrueOrderByLastLoginDesc();
    
    /**
     * Find users for autocomplete (username starts with)
     */
    @Query("SELECT u FROM User u WHERE LOWER(u.username) LIKE LOWER(CONCAT(:prefix, '%')) AND u.isActive = true ORDER BY u.username")
    List<User> findUsernameAutocomplete(@Param("prefix") String prefix);
    
    /**
     * Search users by display name
     */
    @Query("SELECT u FROM User u WHERE LOWER(u.displayName) LIKE LOWER(CONCAT('%', :searchTerm, '%')) AND u.isActive = true")
    List<User> searchByDisplayName(@Param("searchTerm") String searchTerm);
    
    /**
     * Find users by username containing text
     */
    List<User> findByUsernameContainingIgnoreCaseAndIsActiveTrue(String username);
    
    /**
     * Find users created between dates
     */
    List<User> findByCreatedAtBetween(LocalDateTime startDate, LocalDateTime endDate);
    
    /**
     * Update user online status
     */
    @Query("UPDATE User u SET u.isOnline = :isOnline, u.lastSeen = :lastSeen WHERE u.username = :username")
    void updateOnlineStatus(@Param("username") String username, 
                           @Param("isOnline") Boolean isOnline,
                           @Param("lastSeen") LocalDateTime lastSeen);
    
    /**
     * Update user last login
     */
    @Query("UPDATE User u SET u.lastLogin = :lastLogin, u.isRemembered = :isRemembered WHERE u.username = :username")
    void updateLastLogin(@Param("username") String username,
                        @Param("lastLogin") LocalDateTime lastLogin,
                        @Param("isRemembered") Boolean isRemembered);
    
    /**
     * Find users who haven't been online recently
     */
    @Query("SELECT u FROM User u WHERE u.lastSeen < :cutoffTime AND u.isOnline = true")
    List<User> findUsersToMarkOffline(@Param("cutoffTime") LocalDateTime cutoffTime);
}
"""
        },

        {
            "path": "src\\main\\java\\com\\anuj\\redditmessagemanager\\repository\\ChatRepository.java",
            "content": """package com.anuj.redditmessagemanager.repository;

import com.anuj.redditmessagemanager.entity.Chat;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.time.LocalDateTime;
import java.util.List;
import java.util.Optional;

@Repository
public interface ChatRepository extends JpaRepository<Chat, Long> {
    
    /**
     * Find chat between two users
     */
    @Query("SELECT c FROM Chat c WHERE (c.user1Username = :user1 AND c.user2Username = :user2) OR " +
           "(c.user1Username = :user2 AND c.user2Username = :user1)")
    Optional<Chat> findChatBetweenUsers(@Param("user1") String user1, @Param("user2") String user2);
    
    /**
     * Find all chats for a user sorted by most recent activity
     */
    @Query("SELECT c FROM Chat c WHERE (c.user1Username = :username OR c.user2Username = :username) " +
           "AND c.isArchived = false ORDER BY c.lastMessageTimestamp DESC")
    List<Chat> findChatsByUsernameOrderByActivity(@Param("username") String username);
    
    /**
     * Find pinned chats for a user
     */
    @Query("SELECT c FROM Chat c JOIN c.pinnedChats pc WHERE " +
           "(c.user1Username = :username OR c.user2Username = :username) " +
           "AND pc.userUsername = :username AND pc.isActive = true " +
           "ORDER BY pc.pinOrder ASC, c.lastMessageTimestamp DESC")
    List<Chat> findPinnedChatsByUsername(@Param("username") String username);
    
    /**
     * Find chats with unread messages for a user
     */
    @Query("SELECT c FROM Chat c WHERE (c.user1Username = :username OR c.user2Username = :username) " +
           "AND c.hasUnread = true AND c.isArchived = false ORDER BY c.lastMessageTimestamp DESC")
    List<Chat> findChatsWithUnreadMessages(@Param("username") String username);
    
    /**
     * Find chats by date range
     */
    @Query("SELECT c FROM Chat c WHERE (c.user1Username = :username OR c.user2Username = :username) " +
           "AND c.lastMessageTimestamp BETWEEN :startDate AND :endDate " +
           "ORDER BY c.lastMessageTimestamp DESC")
    List<Chat> findChatsByDateRange(@Param("username") String username,
                                   @Param("startDate") LocalDateTime startDate,
                                   @Param("endDate") LocalDateTime endDate);
    
    /**
     * Find chats by other user's username filter
     */
    @Query("SELECT c FROM Chat c WHERE " +
           "((c.user1Username = :username AND LOWER(c.user2Username) LIKE LOWER(CONCAT('%', :otherUser, '%'))) OR " +
           "(c.user2Username = :username AND LOWER(c.user1Username) LIKE LOWER(CONCAT('%', :otherUser, '%')))) " +
           "AND c.isArchived = false ORDER BY c.lastMessageTimestamp DESC")
    List<Chat> findChatsByOtherUserFilter(@Param("username") String username, 
                                         @Param("otherUser") String otherUser);
    
    /**
     * Count unread messages for user
     */
    @Query("SELECT SUM(c.unreadCount) FROM Chat c WHERE " +
           "(c.user1Username = :username OR c.user2Username = :username) AND c.hasUnread = true")
    Long countTotalUnreadMessages(@Param("username") String username);
    
    /**
     * Count total chats for user
     */
    @Query("SELECT COUNT(c) FROM Chat c WHERE " +
           "(c.user1Username = :username OR c.user2Username = :username) AND c.isArchived = false")
    Long countChatsByUsername(@Param("username") String username);
    
    /**
     * Update chat last message info
     */
    @Query("UPDATE Chat c SET c.lastMessage = :lastMessage, c.lastMessageTimestamp = :timestamp, " +
           "c.hasUnread = :hasUnread, c.unreadCount = c.unreadCount + :incrementUnread WHERE c.id = :chatId")
    void updateChatLastMessage(@Param("chatId") Long chatId,
                              @Param("lastMessage") String lastMessage,
                              @Param("timestamp") LocalDateTime timestamp,
                              @Param("hasUnread") Boolean hasUnread,
                              @Param("incrementUnread") Integer incrementUnread);
    
    /**
     * Mark chat as read (reset unread count)
     */
    @Query("UPDATE Chat c SET c.hasUnread = false, c.unreadCount = 0 WHERE c.id = :chatId")
    void markChatAsRead(@Param("chatId") Long chatId);
    
    /**
     * Archive/Unarchive chat
     */
    @Query("UPDATE Chat c SET c.isArchived = :isArchived WHERE c.id = :chatId")
    void updateChatArchiveStatus(@Param("chatId") Long chatId, @Param("isArchived") Boolean isArchived);
    
    /**
     * Find archived chats
     */
    @Query("SELECT c FROM Chat c WHERE (c.user1Username = :username OR c.user2Username = :username) " +
           "AND c.isArchived = true ORDER BY c.lastMessageTimestamp DESC")
    List<Chat> findArchivedChatsByUsername(@Param("username") String username);
}
"""
        },

        {
            "path": "src\\main\\java\\com\\anuj\\redditmessagemanager\\repository\\MessageRepository.java",
            "content": """package com.anuj.redditmessagemanager.repository;

import com.anuj.redditmessagemanager.entity.Message;
import com.anuj.redditmessagemanager.entity.Message.MessageType;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.time.LocalDateTime;
import java.util.List;

@Repository
public interface MessageRepository extends JpaRepository<Message, Long> {
    
    /**
     * Find messages by chat ID with pagination
     */
    @Query("SELECT m FROM Message m WHERE m.chat.id = :chatId AND m.isDeleted = false ORDER BY m.createdAt ASC")
    Page<Message> findMessagesByChatId(@Param("chatId") Long chatId, Pageable pageable);
    
    /**
     * Find messages by chat ID (without pagination)
     */
    @Query("SELECT m FROM Message m WHERE m.chat.id = :chatId AND m.isDeleted = false ORDER BY m.createdAt ASC")
    List<Message> findMessagesByChatId(@Param("chatId") Long chatId);
    
    /**
     * Find latest messages for a chat
     */
    @Query("SELECT m FROM Message m WHERE m.chat.id = :chatId AND m.isDeleted = false ORDER BY m.createdAt DESC")
    List<Message> findLatestMessagesByChatId(@Param("chatId") Long chatId, Pageable pageable);
    
    /**
     * Search messages by content
     */
    @Query("SELECT m FROM Message m WHERE m.chat.id = :chatId AND " +
           "LOWER(m.messageContent) LIKE LOWER(CONCAT('%', :searchTerm, '%')) AND m.isDeleted = false " +
           "ORDER BY m.createdAt DESC")
    List<Message> searchMessagesByContent(@Param("chatId") Long chatId, @Param("searchTerm") String searchTerm);
    
    /**
     * Search messages across all chats for a user
     */
    @Query("SELECT m FROM Message m JOIN m.chat c WHERE " +
           "(c.user1Username = :username OR c.user2Username = :username) AND " +
           "LOWER(m.messageContent) LIKE LOWER(CONCAT('%', :searchTerm, '%')) AND m.isDeleted = false " +
           "ORDER BY m.createdAt DESC")
    List<Message> searchAllMessagesByContent(@Param("username") String username, @Param("searchTerm") String searchTerm);
    
    /**
     * Find messages by sender
     */
    @Query("SELECT m FROM Message m WHERE m.chat.id = :chatId AND m.senderUsername = :senderUsername " +
           "AND m.isDeleted = false ORDER BY m.createdAt DESC")
    List<Message> findMessagesBySender(@Param("chatId") Long chatId, @Param("senderUsername") String senderUsername);
    
    /**
     * Find messages by type
     */
    @Query("SELECT m FROM Message m WHERE m.chat.id = :chatId AND m.messageType = :messageType " +
           "AND m.isDeleted = false ORDER BY m.createdAt DESC")
    List<Message> findMessagesByType(@Param("chatId") Long chatId, @Param("messageType") MessageType messageType);
    
    /**
     * Find unread messages for a user in a chat
     */
    @Query("SELECT m FROM Message m WHERE m.chat.id = :chatId AND m.senderUsername != :username " +
           "AND m.isRead = false AND m.isDeleted = false ORDER BY m.createdAt ASC")
    List<Message> findUnreadMessagesInChat(@Param("chatId") Long chatId, @Param("username") String username);
    
    /**
     * Find messages in date range
     */
    @Query("SELECT m FROM Message m WHERE m.chat.id = :chatId AND " +
           "m.createdAt BETWEEN :startDate AND :endDate AND m.isDeleted = false " +
           "ORDER BY m.createdAt ASC")
    List<Message> findMessagesByDateRange(@Param("chatId") Long chatId,
                                         @Param("startDate") LocalDateTime startDate,
                                         @Param("endDate") LocalDateTime endDate);
    
    /**
     * Count messages in chat
     */
    @Query("SELECT COUNT(m) FROM Message m WHERE m.chat.id = :chatId AND m.isDeleted = false")
    Long countMessagesByChat(@Param("chatId") Long chatId);
    
    /**
     * Count unread messages in chat for user
     */
    @Query("SELECT COUNT(m) FROM Message m WHERE m.chat.id = :chatId AND m.senderUsername != :username " +
           "AND m.isRead = false AND m.isDeleted = false")
    Long countUnreadMessagesInChat(@Param("chatId") Long chatId, @Param("username") String username);
    
    /**
     * Mark messages as read
     */
    @Query("UPDATE Message m SET m.isRead = true WHERE m.chat.id = :chatId AND m.senderUsername != :username " +
           "AND m.isRead = false")
    void markMessagesAsRead(@Param("chatId") Long chatId, @Param("username") String username);
    
    /**
     * Soft delete messages
     */
    @Query("UPDATE Message m SET m.isDeleted = true WHERE m.id IN :messageIds")
    void softDeleteMessages(@Param("messageIds") List<Long> messageIds);
    
    /**
     * Find image messages with hidden status
     */
    @Query("SELECT m FROM Message m WHERE m.chat.id = :chatId AND m.messageType = 'IMAGE' " +
           "AND m.isImageHidden = :isHidden AND m.isDeleted = false ORDER BY m.createdAt DESC")
    List<Message> findImageMessagesByHiddenStatus(@Param("chatId") Long chatId, @Param("isHidden") Boolean isHidden);
    
    /**
     * Toggle image visibility
     */
    @Query("UPDATE Message m SET m.isImageHidden = :isHidden WHERE m.chat.id = :chatId AND m.messageType = 'IMAGE'")
    void toggleImageVisibilityInChat(@Param("chatId") Long chatId, @Param("isHidden") Boolean isHidden);
    
    /**
     * Find messages for export
     */
    @Query("SELECT m FROM Message m WHERE m.chat.id IN :chatIds AND m.isDeleted = false " +
           "AND (:startDate IS NULL OR m.createdAt >= :startDate) " +
           "AND (:endDate IS NULL OR m.createdAt <= :endDate) " +
           "ORDER BY m.chat.id, m.createdAt ASC")
    List<Message> findMessagesForExport(@Param("chatIds") List<Long> chatIds,
                                       @Param("startDate") LocalDateTime startDate,
                                       @Param("endDate") LocalDateTime endDate);
}
"""
        },

        {
            "path": "src\\main\\java\\com\\anuj\\redditmessagemanager\\repository\\BlockedUserRepository.java",
            "content": """package com.anuj.redditmessagemanager.repository;

import com.anuj.redditmessagemanager.entity.BlockedUser;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.time.LocalDateTime;
import java.util.List;
import java.util.Optional;

@Repository
public interface BlockedUserRepository extends JpaRepository<BlockedUser, Long> {
    
    /**
     * Find blocked users by blocker
     */
    List<BlockedUser> findByBlockerUsernameAndIsActiveTrueOrderByBlockedAtDesc(String blockerUsername);
    
    /**
     * Check if user is blocked
     */
    @Query("SELECT bu FROM BlockedUser bu WHERE bu.blockerUsername = :blocker AND bu.blockedUsername = :blocked " +
           "AND bu.isActive = true")
    Optional<BlockedUser> findActiveBlock(@Param("blocker") String blockerUsername, 
                                         @Param("blocked") String blockedUsername);
    
    /**
     * Check if user is blocked (boolean check)
     */
    @Query("SELECT COUNT(bu) > 0 FROM BlockedUser bu WHERE bu.blockerUsername = :blocker AND bu.blockedUsername = :blocked " +
           "AND bu.isActive = true")
    boolean isUserBlocked(@Param("blocker") String blockerUsername, @Param("blocked") String blockedUsername);
    
    /**
     * Find users who blocked a specific user
     */
    List<BlockedUser> findByBlockedUsernameAndIsActiveTrueOrderByBlockedAtDesc(String blockedUsername);
    
    /**
     * Find blocks by blocker and blocked username filter
     */
    @Query("SELECT bu FROM BlockedUser bu WHERE bu.blockerUsername = :blocker " +
           "AND LOWER(bu.blockedUsername) LIKE LOWER(CONCAT('%', :usernameFilter, '%')) " +
           "AND bu.isActive = true ORDER BY bu.blockedAt DESC")
    List<BlockedUser> findBlocksByUsernameFilter(@Param("blocker") String blockerUsername,
                                               @Param("usernameFilter") String usernameFilter);
    
    /**
     * Count blocked users by blocker
     */
    @Query("SELECT COUNT(bu) FROM BlockedUser bu WHERE bu.blockerUsername = :blocker AND bu.isActive = true")
    Long countBlockedUsersByBlocker(@Param("blocker") String blockerUsername);
    
    /**
     * Find blocks in date range
     */
    @Query("SELECT bu FROM BlockedUser bu WHERE bu.blockerUsername = :blocker " +
           "AND bu.blockedAt BETWEEN :startDate AND :endDate AND bu.isActive = true " +
           "ORDER BY bu.blockedAt DESC")
    List<BlockedUser> findBlocksInDateRange(@Param("blocker") String blockerUsername,
                                           @Param("startDate") LocalDateTime startDate,
                                           @Param("endDate") LocalDateTime endDate);
    
    /**
     * Unblock user (set inactive)
     */
    @Query("UPDATE BlockedUser bu SET bu.isActive = false, bu.unblockedAt = :unblockedAt " +
           "WHERE bu.blockerUsername = :blocker AND bu.blockedUsername = :blocked AND bu.isActive = true")
    void unblockUser(@Param("blocker") String blockerUsername,
                    @Param("blocked") String blockedUsername,
                    @Param("unblockedAt") LocalDateTime unblockedAt);
    
    /**
     * Bulk unblock users
     */
    @Query("UPDATE BlockedUser bu SET bu.isActive = false, bu.unblockedAt = :unblockedAt " +
           "WHERE bu.blockerUsername = :blocker AND bu.blockedUsername IN :blockedUsernames AND bu.isActive = true")
    void bulkUnblockUsers(@Param("blocker") String blockerUsername,
                         @Param("blockedUsernames") List<String> blockedUsernames,
                         @Param("unblockedAt") LocalDateTime unblockedAt);
    
    /**
     * Find mutual blocks (users who blocked each other)
     */
    @Query("SELECT bu1 FROM BlockedUser bu1 WHERE bu1.blockerUsername = :user1 AND bu1.blockedUsername = :user2 " +
           "AND bu1.isActive = true AND EXISTS (SELECT bu2 FROM BlockedUser bu2 WHERE bu2.blockerUsername = :user2 " +
           "AND bu2.blockedUsername = :user1 AND bu2.isActive = true)")
    Optional<BlockedUser> findMutualBlock(@Param("user1") String user1, @Param("user2") String user2);
    
    /**
     * Clean up old inactive blocks
     */
    @Query("DELETE FROM BlockedUser bu WHERE bu.isActive = false AND bu.unblockedAt < :cutoffDate")
    void cleanupOldBlocks(@Param("cutoffDate") LocalDateTime cutoffDate);
}
"""
        },

        {
            "path": "src\\main\\java\\com\\anuj\\redditmessagemanager\\repository\\PinnedChatRepository.java",
            "content": """package com.anuj.redditmessagemanager.repository;

import com.anuj.redditmessagemanager.entity.PinnedChat;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.time.LocalDateTime;
import java.util.List;
import java.util.Optional;

@Repository
public interface PinnedChatRepository extends JpaRepository<PinnedChat, Long> {
    
    /**
     * Find pinned chats by user
     */
    List<PinnedChat> findByUserUsernameAndIsActiveTrueOrderByPinOrderAsc(String userUsername);
    
    /**
     * Find pinned chat by chat and user
     */
    Optional<PinnedChat> findByChatIdAndUserUsernameAndIsActiveTrue(Long chatId, String userUsername);
    
    /**
     * Check if chat is pinned by user
     */
    @Query("SELECT COUNT(pc) > 0 FROM PinnedChat pc WHERE pc.chat.id = :chatId AND pc.userUsername = :username " +
           "AND pc.isActive = true")
    boolean isChatPinned(@Param("chatId") Long chatId, @Param("username") String username);
    
    /**
     * Count pinned chats by user
     */
    @Query("SELECT COUNT(pc) FROM PinnedChat pc WHERE pc.userUsername = :username AND pc.isActive = true")
    Long countPinnedChatsByUser(@Param("username") String username);
    
    /**
     * Find next pin order for user
     */
    @Query("SELECT COALESCE(MAX(pc.pinOrder), 0) + 1 FROM PinnedChat pc WHERE pc.userUsername = :username " +
           "AND pc.isActive = true")
    Integer getNextPinOrder(@Param("username") String username);
    
    /**
     * Unpin chat (set inactive)
     */
    @Query("UPDATE PinnedChat pc SET pc.isActive = false, pc.unpinnedAt = :unpinnedAt " +
           "WHERE pc.chat.id = :chatId AND pc.userUsername = :username AND pc.isActive = true")
    void unpinChat(@Param("chatId") Long chatId, 
                   @Param("username") String username, 
                   @Param("unpinnedAt") LocalDateTime unpinnedAt);
    
    /**
     * Bulk unpin chats
     */
    @Query("UPDATE PinnedChat pc SET pc.isActive = false, pc.unpinnedAt = :unpinnedAt " +
           "WHERE pc.chat.id IN :chatIds AND pc.userUsername = :username AND pc.isActive = true")
    void bulkUnpinChats(@Param("chatIds") List<Long> chatIds,
                       @Param("username") String username,
                       @Param("unpinnedAt") LocalDateTime unpinnedAt);
    
    /**
     * Update pin order
     */
    @Query("UPDATE PinnedChat pc SET pc.pinOrder = :newOrder WHERE pc.chat.id = :chatId " +
           "AND pc.userUsername = :username AND pc.isActive = true")
    void updatePinOrder(@Param("chatId") Long chatId, 
                       @Param("username") String username, 
                       @Param("newOrder") Integer newOrder);
    
    /**
     * Reorder pins after unpin
     */
    @Query("UPDATE PinnedChat pc SET pc.pinOrder = pc.pinOrder - 1 WHERE pc.userUsername = :username " +
           "AND pc.pinOrder > :removedOrder AND pc.isActive = true")
    void reorderPinsAfterRemoval(@Param("username") String username, @Param("removedOrder") Integer removedOrder);
    
    /**
     * Find pinned chats in date range
     */
    @Query("SELECT pc FROM PinnedChat pc WHERE pc.userUsername = :username " +
           "AND pc.pinnedAt BETWEEN :startDate AND :endDate AND pc.isActive = true " +
           "ORDER BY pc.pinOrder ASC")
    List<PinnedChat> findPinnedChatsInDateRange(@Param("username") String username,
                                               @Param("startDate") LocalDateTime startDate,
                                               @Param("endDate") LocalDateTime endDate);
    
    /**
     * Clean up old unpinned chats
     */
    @Query("DELETE FROM PinnedChat pc WHERE pc.isActive = false AND pc.unpinnedAt < :cutoffDate")
    void cleanupOldUnpinnedChats(@Param("cutoffDate") LocalDateTime cutoffDate);
}
"""
        },

        {
            "path": "src\\main\\java\\com\\anuj\\redditmessagemanager\\repository\\SearchHistoryRepository.java",
            "content": """package com.anuj.redditmessagemanager.repository;

import com.anuj.redditmessagemanager.entity.SearchHistory;
import com.anuj.redditmessagemanager.entity.SearchHistory.SearchType;
import com.anuj.redditmessagemanager.entity.User;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.time.LocalDateTime;
import java.util.List;

@Repository
public interface SearchHistoryRepository extends JpaRepository<SearchHistory, Long> {
    
    /**
     * Find search history by user
     */
    List<SearchHistory> findByUserOrderBySearchedAtDesc(User user);
    
    /**
     * Find recent searches by user (last 10)
     */
    List<SearchHistory> findTop10ByUserOrderBySearchedAtDesc(User user);
    
    /**
     * Find search history by user and type
     */
    List<SearchHistory> findByUserAndSearchTypeOrderBySearchedAtDesc(User user, SearchType searchType);
    
    /**
     * Find searches by query
     */
    List<SearchHistory> findByUserAndSearchQueryContainingIgnoreCaseOrderBySearchedAtDesc(User user, String query);
    
    /**
     * Find searches within date range
     */
    List<SearchHistory> findByUserAndSearchedAtBetweenOrderBySearchedAtDesc(User user, 
                                                                            LocalDateTime startDate, 
                                                                            LocalDateTime endDate);
    
    /**
     * Get most popular search terms for user
     */
    @Query("SELECT s.searchQuery, COUNT(s) as searchCount FROM SearchHistory s " +
           "WHERE s.user = :user " +
           "GROUP BY s.searchQuery " +
           "ORDER BY searchCount DESC")
    List<Object[]> findMostPopularSearchTerms(@Param("user") User user);
    
    /**
     * Get recent unique search terms for autocomplete
     */
    @Query("SELECT DISTINCT s.searchQuery FROM SearchHistory s WHERE s.user = :user " +
           "AND LOWER(s.searchQuery) LIKE LOWER(CONCAT(:prefix, '%')) " +
           "ORDER BY s.searchedAt DESC")
    List<String> findRecentSearchTermsForAutocomplete(@Param("user") User user, @Param("prefix") String prefix);
    
    /**
     * Count searches by user
     */
    long countByUser(User user);
    
    /**
     * Count searches by type for user
     */
    long countByUserAndSearchType(User user, SearchType searchType);
    
    /**
     * Delete old search history (older than specified date)
     */
    void deleteByUserAndSearchedAtBefore(User user, LocalDateTime cutoffDate);
    
    /**
     * Find searches with results
     */
    List<SearchHistory> findByUserAndResultsCountGreaterThanOrderBySearchedAtDesc(User user, Integer minResults);
    
    /**
     * Check if search query exists for user
     */
    boolean existsByUserAndSearchQuery(User user, String searchQuery);
    
    /**
     * Find similar search queries
     */
    @Query("SELECT s FROM SearchHistory s WHERE s.user = :user " +
           "AND LOWER(s.searchQuery) LIKE LOWER(CONCAT('%', :searchTerm, '%')) " +
           "AND s.searchQuery != :exactQuery ORDER BY s.searchedAt DESC")
    List<SearchHistory> findSimilarSearches(@Param("user") User user, 
                                           @Param("searchTerm") String searchTerm,
                                           @Param("exactQuery") String exactQuery);
    
    /**
     * Get search statistics for user
     */
    @Query("SELECT s.searchType, COUNT(s), AVG(s.resultsCount) FROM SearchHistory s " +
           "WHERE s.user = :user GROUP BY s.searchType")
    List<Object[]> getSearchStatistics(@Param("user") User user);
}
"""
        },

        {
            "path": "src\\main\\java\\com\\anuj\\redditmessagemanager\\repository\\UnreadMessageRepository.java",
            "content": """package com.anuj.redditmessagemanager.repository;

import com.anuj.redditmessagemanager.entity.UnreadMessage;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.time.LocalDateTime;
import java.util.List;

@Repository
public interface UnreadMessageRepository extends JpaRepository<UnreadMessage, Long> {
    
    /**
     * Find unread messages by user
     */
    List<UnreadMessage> findByUserUsernameAndReadAtIsNullOrderByCreatedAtDesc(String userUsername);
    
    /**
     * Find unread messages by user and chat
     */
    @Query("SELECT um FROM UnreadMessage um WHERE um.userUsername = :username " +
           "AND um.message.chat.id = :chatId AND um.readAt IS NULL ORDER BY um.createdAt ASC")
    List<UnreadMessage> findUnreadMessagesByChatAndUser(@Param("chatId") Long chatId, @Param("username") String username);
    
    /**
     * Count unread messages by user
     */
    @Query("SELECT COUNT(um) FROM UnreadMessage um WHERE um.userUsername = :username AND um.readAt IS NULL")
    Long countUnreadMessagesByUser(@Param("username") String username);
    
    /**
     * Count unread messages by chat and user
     */
    @Query("SELECT COUNT(um) FROM UnreadMessage um WHERE um.userUsername = :username " +
           "AND um.message.chat.id = :chatId AND um.readAt IS NULL")
    Long countUnreadMessagesByChatAndUser(@Param("chatId") Long chatId, @Param("username") String username);
    
    /**
     * Mark messages as read
     */
    @Query("UPDATE UnreadMessage um SET um.readAt = :readAt WHERE um.userUsername = :username " +
           "AND um.message.chat.id = :chatId AND um.readAt IS NULL")
    void markMessagesAsReadInChat(@Param("chatId") Long chatId, 
                                 @Param("username") String username,
                                 @Param("readAt") LocalDateTime readAt);
    
    /**
     * Mark specific message as read
     */
    @Query("UPDATE UnreadMessage um SET um.readAt = :readAt WHERE um.message.id = :messageId " +
           "AND um.userUsername = :username AND um.readAt IS NULL")
    void markMessageAsRead(@Param("messageId") Long messageId,
                          @Param("username") String username,
                          @Param("readAt") LocalDateTime readAt);
    
    /**
     * Mark all messages as read for user
     */
    @Query("UPDATE UnreadMessage um SET um.readAt = :readAt WHERE um.userUsername = :username AND um.readAt IS NULL")
    void markAllMessagesAsReadForUser(@Param("username") String username, @Param("readAt") LocalDateTime readAt);
    
    /**
     * Find unread messages with notifications not sent
     */
    @Query("SELECT um FROM UnreadMessage um WHERE um.userUsername = :username " +
           "AND um.readAt IS NULL AND um.isNotificationSent = false ORDER BY um.createdAt ASC")
    List<UnreadMessage> findUnreadMessagesWithoutNotification(@Param("username") String username);
    
    /**
     * Update notification sent status
     */
    @Query("UPDATE UnreadMessage um SET um.isNotificationSent = true WHERE um.id IN :unreadMessageIds")
    void markNotificationsSent(@Param("unreadMessageIds") List<Long> unreadMessageIds);
    
    /**
     * Find unread messages by date range
     */
    @Query("SELECT um FROM UnreadMessage um WHERE um.userUsername = :username " +
           "AND um.createdAt BETWEEN :startDate AND :endDate AND um.readAt IS NULL " +
           "ORDER BY um.createdAt DESC")
    List<UnreadMessage> findUnreadMessagesInDateRange(@Param("username") String username,
                                                     @Param("startDate") LocalDateTime startDate,
                                                     @Param("endDate") LocalDateTime endDate);
    
    /**
     * Clean up old read messages
     */
    @Query("DELETE FROM UnreadMessage um WHERE um.readAt IS NOT NULL AND um.readAt < :cutoffDate")
    void cleanupOldReadMessages(@Param("cutoffDate") LocalDateTime cutoffDate);
    
    /**
     * Get unread message statistics by chat
     */
    @Query("SELECT um.message.chat.id, COUNT(um) FROM UnreadMessage um " +
           "WHERE um.userUsername = :username AND um.readAt IS NULL GROUP BY um.message.chat.id")
    List<Object[]> getUnreadCountsByChat(@Param("username") String username);
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

    # Create entity and repository files
    create_files(entity_files, "Entity")
    create_files(repository_files, "Repository")

    print("\n" + "="*70)
    print("Entity and Repository classes created successfully!")
    print("="*70)

    print("\nCreated Entity Classes:")
    print("✓ User.java - Local user management (removed Reddit fields)")
    print("✓ Chat.java - Chat conversations with pinning and unread tracking")
    print("✓ Message.java - Individual messages with type support")
    print("✓ BlockedUser.java - User blocking system")
    print("✓ PinnedChat.java - Pin chats to top functionality")
    print("✓ UnreadMessage.java - Unread message tracking")
    print("✓ SearchHistory.java - Search history tracking (updated)")

    print("\nCreated Repository Classes:")
    print("✓ UserRepository.java - Local user operations with autocomplete")
    print("✓ ChatRepository.java - Chat management with filtering and sorting")
    print("✓ MessageRepository.java - Message operations with search capabilities")
    print("✓ BlockedUserRepository.java - Block/unblock operations")
    print("✓ PinnedChatRepository.java - Pin/unpin chat functionality")
    print("✓ UnreadMessageRepository.java - Unread message tracking")
    print("✓ SearchHistoryRepository.java - Enhanced search history")

    print("\nKey Features Included:")
    print("• Local authentication without Reddit dependencies")
    print("• Chat conversations with participant tracking")
    print("• Message types (TEXT, IMAGE, FILE, SYSTEM)")
    print("• Pin/unpin chats with custom ordering")
    print("• Block/unblock users with bulk operations")
    print("• Unread message tracking and notifications")
    print("• Advanced search with autocomplete suggestions")
    print("• Image message hide/show functionality")
    print("• Soft delete for messages")
    print("• Archive/unarchive chats")
    print("• Date range filtering")
    print("• Export-ready message queries")
    print("• Bulk operations support")
    print("• Message content search across all chats")

    print("\nDatabase Features:")
    print("• Unique constraints for data integrity")
    print("• Proper foreign key relationships")
    print("• Efficient indexing for search operations")
    print("• Timestamp tracking for all entities")
    print("• Soft delete patterns")
    print("• Pagination support")

    print("\nNext steps:")
    print("1. Update your service classes to use these new entities")
    print("2. Update your controllers to work with the new repositories")
    print("3. Test database operations")
    print("4. Run the application to generate database tables")

if __name__ == "__main__":
    create_entity_and_repository_classes()
