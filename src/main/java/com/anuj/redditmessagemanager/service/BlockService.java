package com.anuj.redditmessagemanager.service;

import com.anuj.redditmessagemanager.dto.BlockedUserDto;
import com.anuj.redditmessagemanager.entity.BlockedUser;
import com.anuj.redditmessagemanager.entity.User;
import com.anuj.redditmessagemanager.repository.BlockedUserRepository;
import com.anuj.redditmessagemanager.repository.UserRepository;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.util.List;
import java.util.stream.Collectors;

@Service
@Transactional
public class BlockService {
    
    private static final Logger logger = LoggerFactory.getLogger(BlockService.class);
    
    @Autowired
    private BlockedUserRepository blockedUserRepository;
    
    @Autowired
    private UserRepository userRepository;
    
    /**
     * Block a user
     */
    public BlockedUserDto blockUser(String blockerUsername, BlockedUserDto blockRequest) {
        try {
            String blockedUsername = blockRequest.getBlockedUsername();
            String reason = blockRequest.getReason();
            
            // Validate users exist
            User blocker = userRepository.findByUsername(blockerUsername).orElse(null);
            User blocked = userRepository.findByUsername(blockedUsername).orElse(null);
            
            if (blocker == null) {
                throw new RuntimeException("Blocker user not found");
            }
            if (blocked == null) {
                throw new RuntimeException("User to block not found");
            }
            if (blockerUsername.equals(blockedUsername)) {
                throw new RuntimeException("Cannot block yourself");
            }
            
            // Check if already blocked
            if (blockedUserRepository.isUserBlocked(blockerUsername, blockedUsername)) {
                throw new RuntimeException("User is already blocked");
            }
            
            // Create block entry
            BlockedUser blockedUser = new BlockedUser();
            blockedUser.setBlockerUsername(blockerUsername);
            blockedUser.setBlockedUsername(blockedUsername);
            blockedUser.setReason(reason != null ? reason.trim() : "No reason provided");
            blockedUser.setIsActive(true);
            
            BlockedUser savedBlock = blockedUserRepository.save(blockedUser);
            
            logger.info("User {} blocked user {} with reason: {}", 
                blockerUsername, blockedUsername, reason);
            
            return convertToDto(savedBlock);
            
        } catch (Exception e) {
            logger.error("Error blocking user: {}", e.getMessage());
            throw new RuntimeException("Failed to block user: " + e.getMessage(), e);
        }
    }
    
    /**
     * Unblock a user
     */
    public boolean unblockUser(String blockerUsername, String blockedUsername) {
        try {
            BlockedUser blockedUser = blockedUserRepository
                .findActiveBlock(blockerUsername, blockedUsername).orElse(null);
            
            if (blockedUser == null) {
                return false; // User was not blocked
            }
            
            blockedUserRepository.unblockUser(blockerUsername, blockedUsername, LocalDateTime.now());
            
            logger.info("User {} unblocked user {}", blockerUsername, blockedUsername);
            return true;
            
        } catch (Exception e) {
            logger.error("Error unblocking user: {}", e.getMessage());
            throw new RuntimeException("Failed to unblock user: " + e.getMessage(), e);
        }
    }
    
    /**
     * Get list of blocked users for a user
     */
    public List<BlockedUserDto> getBlockedUsers(String blockerUsername) {
        try {
            List<BlockedUser> blockedUsers = blockedUserRepository
                .findByBlockerUsernameAndIsActiveTrueOrderByBlockedAtDesc(blockerUsername);
            
            return blockedUsers.stream()
                    .map(this::convertToDto)
                    .collect(Collectors.toList());
                    
        } catch (Exception e) {
            logger.error("Error getting blocked users: {}", e.getMessage());
            return List.of();
        }
    }
    
    /**
     * Bulk unblock users
     */
    public int bulkUnblockUsers(String blockerUsername, List<String> blockedUsernames) {
        try {
            if (blockedUsernames == null || blockedUsernames.isEmpty()) {
                return 0;
            }
            
            // Validate that all users are actually blocked by this user
            int validBlocks = 0;
            for (String blockedUsername : blockedUsernames) {
                if (blockedUserRepository.isUserBlocked(blockerUsername, blockedUsername)) {
                    validBlocks++;
                }
            }
            
            if (validBlocks > 0) {
                blockedUserRepository.bulkUnblockUsers(blockerUsername, blockedUsernames, LocalDateTime.now());
                logger.info("User {} bulk unblocked {} users", blockerUsername, validBlocks);
            }
            
            return validBlocks;
            
        } catch (Exception e) {
            logger.error("Error bulk unblocking users: {}", e.getMessage());
            throw new RuntimeException("Failed to bulk unblock users: " + e.getMessage(), e);
        }
    }
    
    /**
     * Check if a user is blocked
     */
    public boolean isUserBlocked(String blockerUsername, String blockedUsername) {
        try {
            return blockedUserRepository.isUserBlocked(blockerUsername, blockedUsername);
        } catch (Exception e) {
            logger.error("Error checking if user is blocked: {}", e.getMessage());
            return false;
        }
    }
    
    /**
     * Search blocked users by username filter
     */
    public List<BlockedUserDto> searchBlockedUsers(String blockerUsername, String usernameFilter) {
        try {
            List<BlockedUser> blockedUsers = blockedUserRepository
                .findBlocksByUsernameFilter(blockerUsername, usernameFilter);
            
            return blockedUsers.stream()
                    .map(this::convertToDto)
                    .collect(Collectors.toList());
                    
        } catch (Exception e) {
            logger.error("Error searching blocked users: {}", e.getMessage());
            return List.of();
        }
    }
    
    /**
     * Get blocked users within date range
     */
    public List<BlockedUserDto> getBlockedUsersInDateRange(String blockerUsername, 
                                                          LocalDateTime startDate, 
                                                          LocalDateTime endDate) {
        try {
            List<BlockedUser> blockedUsers = blockedUserRepository
                .findBlocksInDateRange(blockerUsername, startDate, endDate);
            
            return blockedUsers.stream()
                    .map(this::convertToDto)
                    .collect(Collectors.toList());
                    
        } catch (Exception e) {
            logger.error("Error getting blocked users in date range: {}", e.getMessage());
            return List.of();
        }
    }
    
    /**
     * Get block statistics for user
     */
    public Long getBlockedUserCount(String blockerUsername) {
        try {
            return blockedUserRepository.countBlockedUsersByBlocker(blockerUsername);
        } catch (Exception e) {
            logger.error("Error getting blocked user count: {}", e.getMessage());
            return 0L;
        }
    }
    
    /**
     * Check for mutual blocks (users blocking each other)
     */
    public boolean isMutualBlock(String user1, String user2) {
        try {
            return blockedUserRepository.findMutualBlock(user1, user2).isPresent();
        } catch (Exception e) {
            logger.error("Error checking mutual block: {}", e.getMessage());
            return false;
        }
    }
    
    /**
     * Convert BlockedUser entity to DTO
     */
    private BlockedUserDto convertToDto(BlockedUser blockedUser) {
        BlockedUserDto dto = new BlockedUserDto();
        dto.setId(blockedUser.getId());
        dto.setBlockerUsername(blockedUser.getBlockerUsername());
        dto.setBlockedUsername(blockedUser.getBlockedUsername());
        dto.setReason(blockedUser.getReason());
        dto.setBlockedAt(blockedUser.getBlockedAt());
        dto.setCanUnblock(blockedUser.getIsActive());
        
        // Get blocked user's display name if available
        User blockedUserEntity = userRepository.findByUsername(blockedUser.getBlockedUsername()).orElse(null);
        if (blockedUserEntity != null) {
            dto.setBlockedUserDisplayName(blockedUserEntity.getDisplayName());
            dto.setBlockedUserAvatar(blockedUserEntity.getAvatarUrl());
        }
        
        // Format blocked time for display
        if (blockedUser.getBlockedAt() != null) {
            dto.setFormattedBlockedTime(blockedUser.getBlockedAt()
                .format(DateTimeFormatter.ofPattern("MMM dd, yyyy 'at' HH:mm")));
        }
        
        return dto;
    }
}
