package com.anuj.redditmessagemanager.repository;

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
