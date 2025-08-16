package com.anuj.redditmessagemanager.repository;

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
