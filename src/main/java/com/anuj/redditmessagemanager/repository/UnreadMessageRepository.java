package com.anuj.redditmessagemanager.repository;

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
