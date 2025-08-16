import os

def create_repository_and_entity_code():
    # Base path from your previous conversation
    base_path = "D:\\Karan Ticket Project\\Reddit Message Manager"

    # Entity classes to create
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
    
    @Column(name = "reddit_username", unique = true, nullable = false)
    private String redditUsername;
    
    @Column(name = "reddit_user_id", unique = true)
    private String redditUserId;
    
    @Column(name = "access_token", length = 1000)
    private String accessToken;
    
    @Column(name = "refresh_token", length = 1000)
    private String refreshToken;
    
    @Column(name = "token_expires_at")
    private LocalDateTime tokenExpiresAt;
    
    @Column(name = "is_active")
    private Boolean isActive = true;
    
    @CreationTimestamp
    @Column(name = "created_at")
    private LocalDateTime createdAt;
    
    @UpdateTimestamp
    @Column(name = "updated_at")
    private LocalDateTime updatedAt;
    
    @OneToMany(mappedBy = "user", cascade = CascadeType.ALL, fetch = FetchType.LAZY)
    private List<RedditMessage> messages;
    
    // Custom constructor for creating user during OAuth
    public User(String redditUsername, String redditUserId, String accessToken, String refreshToken) {
        this.redditUsername = redditUsername;
        this.redditUserId = redditUserId;
        this.accessToken = accessToken;
        this.refreshToken = refreshToken;
        this.isActive = true;
    }
}
"""
        },

        {
            "path": "src\\main\\java\\com\\anuj\\redditmessagemanager\\entity\\RedditMessage.java",
            "content": """package com.anuj.redditmessagemanager.entity;

import jakarta.persistence.*;
import lombok.Data;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;
import org.hibernate.annotations.CreationTimestamp;

import java.time.LocalDateTime;

@Entity
@Table(name = "reddit_messages")
@Data
@NoArgsConstructor
@AllArgsConstructor
public class RedditMessage {
    
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    @Column(name = "reddit_message_id", unique = true, nullable = false)
    private String redditMessageId;
    
    @Column(name = "message_type", nullable = false)
    @Enumerated(EnumType.STRING)
    private MessageType messageType;
    
    @Column(name = "subject", length = 500)
    private String subject;
    
    @Column(name = "body", columnDefinition = "TEXT")
    private String body;
    
    @Column(name = "author")
    private String author;
    
    @Column(name = "recipient")
    private String recipient;
    
    @Column(name = "subreddit")
    private String subreddit;
    
    @Column(name = "is_read")
    private Boolean isRead = false;
    
    @Column(name = "reddit_created_at")
    private LocalDateTime redditCreatedAt;
    
    @Column(name = "context")
    private String context;
    
    @Column(name = "parent_id")
    private String parentId;
    
    @CreationTimestamp
    @Column(name = "stored_at")
    private LocalDateTime storedAt;
    
    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "user_id", nullable = false)
    private User user;
    
    // Enum for message types
    public enum MessageType {
        INBOX,
        SENT,
        UNREAD,
        COMMENT_REPLY,
        POST_REPLY,
        USERNAME_MENTION
    }
    
    // Constructor for creating from Reddit API response
    public RedditMessage(String redditMessageId, MessageType messageType, String subject, 
                        String body, String author, String recipient, User user) {
        this.redditMessageId = redditMessageId;
        this.messageType = messageType;
        this.subject = subject;
        this.body = body;
        this.author = author;
        this.recipient = recipient;
        this.user = user;
        this.isRead = false;
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
        POSTS,
        MESSAGES,
        SUBREDDITS,
        USERS
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

    # Repository interfaces to create
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
     * Find user by Reddit username
     */
    Optional<User> findByRedditUsername(String redditUsername);
    
    /**
     * Find user by Reddit user ID
     */
    Optional<User> findByRedditUserId(String redditUserId);
    
    /**
     * Find user by access token
     */
    Optional<User> findByAccessToken(String accessToken);
    
    /**
     * Check if user exists by Reddit username
     */
    boolean existsByRedditUsername(String redditUsername);
    
    /**
     * Find all active users
     */
    List<User> findByIsActiveTrue();
    
    /**
     * Find users with expired tokens
     */
    @Query("SELECT u FROM User u WHERE u.tokenExpiresAt < :currentTime AND u.isActive = true")
    List<User> findUsersWithExpiredTokens(@Param("currentTime") LocalDateTime currentTime);
    
    /**
     * Find users created between dates
     */
    List<User> findByCreatedAtBetween(LocalDateTime startDate, LocalDateTime endDate);
    
    /**
     * Update user's access token and expiry
     */
    @Query("UPDATE User u SET u.accessToken = :accessToken, u.tokenExpiresAt = :expiresAt WHERE u.id = :userId")
    void updateUserToken(@Param("userId") Long userId, 
                        @Param("accessToken") String accessToken, 
                        @Param("expiresAt") LocalDateTime expiresAt);
    
    /**
     * Deactivate user
     */
    @Query("UPDATE User u SET u.isActive = false WHERE u.id = :userId")
    void deactivateUser(@Param("userId") Long userId);
}
"""
        },

        {
            "path": "src\\main\\java\\com\\anuj\\redditmessagemanager\\repository\\RedditMessageRepository.java",
            "content": """package com.anuj.redditmessagemanager.repository;

import com.anuj.redditmessagemanager.entity.RedditMessage;
import com.anuj.redditmessagemanager.entity.RedditMessage.MessageType;
import com.anuj.redditmessagemanager.entity.User;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.time.LocalDateTime;
import java.util.List;
import java.util.Optional;

@Repository
public interface RedditMessageRepository extends JpaRepository<RedditMessage, Long> {
    
    /**
     * Find message by Reddit message ID
     */
    Optional<RedditMessage> findByRedditMessageId(String redditMessageId);
    
    /**
     * Find messages by user
     */
    List<RedditMessage> findByUserOrderByStoredAtDesc(User user);
    
    /**
     * Find messages by user with pagination
     */
    Page<RedditMessage> findByUserOrderByStoredAtDesc(User user, Pageable pageable);
    
    /**
     * Find messages by user and type
     */
    List<RedditMessage> findByUserAndMessageTypeOrderByStoredAtDesc(User user, MessageType messageType);
    
    /**
     * Find unread messages by user
     */
    List<RedditMessage> findByUserAndIsReadFalseOrderByStoredAtDesc(User user);
    
    /**
     * Find messages by author
     */
    List<RedditMessage> findByUserAndAuthorContainingIgnoreCaseOrderByStoredAtDesc(User user, String author);
    
    /**
     * Find messages by subject
     */
    List<RedditMessage> findByUserAndSubjectContainingIgnoreCaseOrderByStoredAtDesc(User user, String subject);
    
    /**
     * Search messages by content
     */
    @Query("SELECT m FROM RedditMessage m WHERE m.user = :user AND " +
           "(LOWER(m.subject) LIKE LOWER(CONCAT('%', :searchTerm, '%')) OR " +
           "LOWER(m.body) LIKE LOWER(CONCAT('%', :searchTerm, '%')) OR " +
           "LOWER(m.author) LIKE LOWER(CONCAT('%', :searchTerm, '%'))) " +
           "ORDER BY m.storedAt DESC")
    List<RedditMessage> searchMessagesByContent(@Param("user") User user, @Param("searchTerm") String searchTerm);
    
    /**
     * Find messages by date range
     */
    List<RedditMessage> findByUserAndStoredAtBetweenOrderByStoredAtDesc(User user, LocalDateTime startDate, LocalDateTime endDate);
    
    /**
     * Count unread messages for user
     */
    long countByUserAndIsReadFalse(User user);
    
    /**
     * Count messages by type for user
     */
    long countByUserAndMessageType(User user, MessageType messageType);
    
    /**
     * Find messages by subreddit
     */
    List<RedditMessage> findByUserAndSubredditContainingIgnoreCaseOrderByStoredAtDesc(User user, String subreddit);
    
    /**
     * Mark message as read
     */
    @Query("UPDATE RedditMessage m SET m.isRead = true WHERE m.id = :messageId AND m.user = :user")
    void markMessageAsRead(@Param("messageId") Long messageId, @Param("user") User user);
    
    /**
     * Mark all messages as read for user
     */
    @Query("UPDATE RedditMessage m SET m.isRead = true WHERE m.user = :user AND m.isRead = false")
    void markAllMessagesAsRead(@Param("user") User user);
    
    /**
     * Delete messages older than specified date
     */
    void deleteByUserAndStoredAtBefore(User user, LocalDateTime cutoffDate);
    
    /**
     * Check if message exists by Reddit ID
     */
    boolean existsByRedditMessageId(String redditMessageId);
    
    /**
     * Find latest message for user
     */
    Optional<RedditMessage> findTopByUserOrderByStoredAtDesc(User user);
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
     * Count searches by user
     */
    long countByUser(User user);
    
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

    # Create entity files
    create_files(entity_files, "Entity")

    # Create repository files
    create_files(repository_files, "Repository")

    print("\n" + "="*60)
    print("Repository and Entity classes created successfully!")
    print("="*60)
    print("\nCreated Entity Classes:")
    print("✓ User.java - Main user entity with OAuth tokens")
    print("✓ RedditMessage.java - Reddit message storage entity")
    print("✓ SearchHistory.java - Search history tracking entity")

    print("\nCreated Repository Interfaces:")
    print("✓ UserRepository.java - User data access methods")
    print("✓ RedditMessageRepository.java - Message data access methods")
    print("✓ SearchHistoryRepository.java - Search history data access methods")

    print("\nFeatures included:")
    print("• Lombok annotations for clean code")
    print("• JPA relationships and constraints")
    print("• Custom query methods")
    print("• Pagination support")
    print("• Search functionality")
    print("• Timestamp tracking")
    print("• Data validation")

    print("\nNext steps:")
    print("1. Create service classes")
    print("2. Create controller classes")
    print("3. Create DTOs for API responses")
    print("4. Test the repository methods")
    print("5. Run the application to generate database tables")

if __name__ == "__main__":
    create_repository_and_entity_code()
