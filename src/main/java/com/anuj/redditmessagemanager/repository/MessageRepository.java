package com.anuj.redditmessagemanager.repository;

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
