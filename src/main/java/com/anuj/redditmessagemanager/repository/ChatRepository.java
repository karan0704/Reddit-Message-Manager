package com.anuj.redditmessagemanager.repository;

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
