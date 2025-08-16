package com.anuj.redditmessagemanager.repository;

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
