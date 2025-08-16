package com.anuj.redditmessagemanager.repository;

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
