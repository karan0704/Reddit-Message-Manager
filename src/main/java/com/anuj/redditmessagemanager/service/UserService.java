package com.anuj.redditmessagemanager.service;

import com.anuj.redditmessagemanager.dto.UserDto;
import com.anuj.redditmessagemanager.entity.User;
import com.anuj.redditmessagemanager.repository.UserRepository;
import com.anuj.redditmessagemanager.repository.ChatRepository;
import com.anuj.redditmessagemanager.repository.MessageRepository;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.time.LocalDateTime;
import java.util.List;
import java.util.stream.Collectors;

@Service
@Transactional
public class UserService {
    
    private static final Logger logger = LoggerFactory.getLogger(UserService.class);
    
    @Autowired
    private UserRepository userRepository;
    
    @Autowired
    private ChatRepository chatRepository;
    
    @Autowired
    private MessageRepository messageRepository;
    
    /**
     * Find user by username
     */
    public User findByUsername(String username) {
        return userRepository.findByUsername(username).orElse(null);
    }
    
    /**
     * Check if user exists by username
     */
    public boolean existsByUsername(String username) {
        return userRepository.existsByUsername(username);
    }
    
    /**
     * Get username autocomplete suggestions
     */
    public List<UserDto> getUsernameAutocomplete(String prefix, String currentUsername) {
        try {
            List<User> users = userRepository.findUsernameAutocomplete(prefix);
            
            return users.stream()
                    .filter(user -> !user.getUsername().equals(currentUsername))
                    .limit(10)
                    .map(this::convertToDto)
                    .collect(Collectors.toList());
                    
        } catch (Exception e) {
            logger.error("Error getting username autocomplete: {}", e.getMessage());
            return List.of();
        }
    }
    
    /**
     * Search users by display name or username
     */
    public List<UserDto> searchUsers(String searchTerm, String currentUsername) {
        try {
            List<User> usersByUsername = userRepository.findByUsernameContainingIgnoreCaseAndIsActiveTrue(searchTerm);
            List<User> usersByDisplayName = userRepository.searchByDisplayName(searchTerm);
            
            // Combine results and remove duplicates
            List<User> allUsers = usersByUsername;
            usersByDisplayName.stream()
                    .filter(user -> !allUsers.contains(user))
                    .forEach(allUsers::add);
            
            return allUsers.stream()
                    .filter(user -> !user.getUsername().equals(currentUsername))
                    .limit(20)
                    .map(this::convertToDto)
                    .collect(Collectors.toList());
                    
        } catch (Exception e) {
            logger.error("Error searching users: {}", e.getMessage());
            return List.of();
        }
    }
    
    /**
     * Update user login information
     */
    public void updateUserLogin(String username, boolean rememberUser) {
        try {
            userRepository.updateLastLogin(username, LocalDateTime.now(), rememberUser);
            userRepository.updateOnlineStatus(username, true, LocalDateTime.now());
            
            logger.info("Updated login info for user: {} (remember: {})", username, rememberUser);
            
        } catch (Exception e) {
            logger.error("Error updating user login: {}", e.getMessage());
        }
    }
    
    /**
     * Update user online status
     */
    public void updateUserOnlineStatus(String username, boolean isOnline) {
        try {
            userRepository.updateOnlineStatus(username, isOnline, LocalDateTime.now());
        } catch (Exception e) {
            logger.error("Error updating online status: {}", e.getMessage());
        }
    }
    
    /**
     * Get remembered users for quick login
     */
    public List<UserDto> getRememberedUsers() {
        try {
            List<User> rememberedUsers = userRepository.findByIsRememberedTrueOrderByLastLoginDesc();
            
            return rememberedUsers.stream()
                    .limit(5) // Limit to last 5 remembered users
                    .map(this::convertToDto)
                    .collect(Collectors.toList());
                    
        } catch (Exception e) {
            logger.error("Error getting remembered users: {}", e.getMessage());
            return List.of();
        }
    }
    
    /**
     * Get user statistics
     */
    public UserDto getUserStatistics(String username) {
        try {
            User user = findByUsername(username);
            if (user == null) {
                return null;
            }
            
            UserDto userDto = convertToDto(user);
            
            // Add chat and message statistics
            userDto.setChatCount(chatRepository.countChatsByUsername(username));
            userDto.setUnreadCount(chatRepository.countTotalUnreadMessages(username));
            
            return userDto;
            
        } catch (Exception e) {
            logger.error("Error getting user statistics: {}", e.getMessage());
            return null;
        }
    }
    
    /**
     * Clean up offline users (mark users offline if inactive)
     */
    public void cleanupOfflineUsers() {
        try {
            LocalDateTime cutoffTime = LocalDateTime.now().minusMinutes(15); // 15 minutes inactive
            List<User> usersToMarkOffline = userRepository.findUsersToMarkOffline(cutoffTime);
            
            for (User user : usersToMarkOffline) {
                userRepository.updateOnlineStatus(user.getUsername(), false, LocalDateTime.now());
            }
            
            if (!usersToMarkOffline.isEmpty()) {
                logger.info("Marked {} users as offline due to inactivity", usersToMarkOffline.size());
            }
            
        } catch (Exception e) {
            logger.error("Error cleaning up offline users: {}", e.getMessage());
        }
    }
    
    /**
     * Convert User entity to DTO
     */
    public UserDto convertToDto(User user) {
        if (user == null) {
            return null;
        }
        
        UserDto dto = new UserDto();
        dto.setId(user.getId());
        dto.setUsername(user.getUsername());
        dto.setDisplayName(user.getDisplayName());
        dto.setEmail(user.getEmail());
        dto.setIsActive(user.getIsActive());
        dto.setIsOnline(user.getIsOnline());
        dto.setLastSeen(user.getLastSeen());
        dto.setCreatedAt(user.getCreatedAt());
        dto.setAvatarUrl(user.getAvatarUrl());
        dto.setIsRemembered(user.getIsRemembered());
        
        return dto;
    }
    
    /**
     * Update user profile
     */
    public User updateUserProfile(String username, String displayName, String email) {
        try {
            User user = findByUsername(username);
            if (user == null) {
                throw new RuntimeException("User not found");
            }
            
            if (displayName != null && !displayName.trim().isEmpty()) {
                user.setDisplayName(displayName.trim());
            }
            
            if (email != null && !email.trim().isEmpty()) {
                // Check if email is already taken by another user
                User existingUser = userRepository.findByEmail(email).orElse(null);
                if (existingUser != null && !existingUser.getId().equals(user.getId())) {
                    throw new RuntimeException("Email already in use");
                }
                user.setEmail(email.trim());
            }
            
            User savedUser = userRepository.save(user);
            logger.info("User profile updated: {}", username);
            return savedUser;
            
        } catch (Exception e) {
            logger.error("Error updating user profile: {}", e.getMessage());
            throw new RuntimeException("Failed to update profile", e);
        }
    }
    
    /**
     * Deactivate user account
     */
    public void deactivateUser(String username) {
        try {
            User user = findByUsername(username);
            if (user != null) {
                user.setIsActive(false);
                user.setIsOnline(false);
                userRepository.save(user);
                
                logger.info("User account deactivated: {}", username);
            }
        } catch (Exception e) {
            logger.error("Error deactivating user: {}", e.getMessage());
            throw new RuntimeException("Failed to deactivate user", e);
        }
    }

    public User findById(Long userId) {//this method should not use
        return userRepository.findById(userId).orElse(null);
    }
}
