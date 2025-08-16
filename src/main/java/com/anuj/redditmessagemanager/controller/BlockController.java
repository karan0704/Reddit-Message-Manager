package com.anuj.redditmessagemanager.controller;

import com.anuj.redditmessagemanager.dto.BlockedUserDto;
import com.anuj.redditmessagemanager.dto.BulkActionDto;
import com.anuj.redditmessagemanager.service.BlockService;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import jakarta.servlet.http.HttpSession;
import java.util.List;
import java.util.Map;

@RestController
@RequestMapping("/api/block")
public class BlockController {
    
    private static final Logger logger = LoggerFactory.getLogger(BlockController.class);
    
    @Autowired
    private BlockService blockService;
    
    /**
     * Block a user
     */
    @PostMapping("/user")
    public ResponseEntity<?> blockUser(@RequestBody BlockedUserDto blockRequest, HttpSession session) {
        try {
            String username = getCurrentUsername(session);
            BlockedUserDto blockedUser = blockService.blockUser(username, blockRequest);
            
            return ResponseEntity.ok(Map.of(
                "success", true,
                "blockedUser", blockedUser,
                "message", "User blocked successfully"
            ));
            
        } catch (Exception e) {
            logger.error("Error blocking user: {}", e.getMessage());
            return ResponseEntity.status(500).body(Map.of(
                "error", "Failed to block user: " + e.getMessage()
            ));
        }
    }
    
    /**
     * Unblock a user
     */
    @DeleteMapping("/user/{blockedUsername}")
    public ResponseEntity<?> unblockUser(@PathVariable String blockedUsername, HttpSession session) {
        try {
            String username = getCurrentUsername(session);
            boolean success = blockService.unblockUser(username, blockedUsername);
            
            if (success) {
                return ResponseEntity.ok(Map.of(
                    "success", true,
                    "message", "User unblocked successfully"
                ));
            } else {
                return ResponseEntity.badRequest().body(Map.of(
                    "error", "User was not blocked or already unblocked"
                ));
            }
            
        } catch (Exception e) {
            logger.error("Error unblocking user: {}", e.getMessage());
            return ResponseEntity.status(500).body(Map.of(
                "error", "Failed to unblock user: " + e.getMessage()
            ));
        }
    }
    
    /**
     * Get list of blocked users
     */
    @GetMapping("/list")
    public ResponseEntity<?> getBlockedUsers(HttpSession session) {
        try {
            String username = getCurrentUsername(session);
            List<BlockedUserDto> blockedUsers = blockService.getBlockedUsers(username);
            
            return ResponseEntity.ok(Map.of(
                "blockedUsers", blockedUsers,
                "count", blockedUsers.size()
            ));
            
        } catch (Exception e) {
            logger.error("Error getting blocked users: {}", e.getMessage());
            return ResponseEntity.status(500).body(Map.of(
                "error", "Failed to get blocked users: " + e.getMessage()
            ));
        }
    }
    
    /**
     * Bulk unblock users
     */
    @PostMapping("/bulk-unblock")
    public ResponseEntity<?> bulkUnblockUsers(@RequestBody BulkActionDto bulkAction, HttpSession session) {
        try {
            String username = getCurrentUsername(session);
            int unblocked = blockService.bulkUnblockUsers(username, bulkAction.getUsernames());
            
            return ResponseEntity.ok(Map.of(
                "success", true,
                "unblockedCount", unblocked,
                "message", unblocked + " users unblocked successfully"
            ));
            
        } catch (Exception e) {
            logger.error("Error bulk unblocking users: {}", e.getMessage());
            return ResponseEntity.status(500).body(Map.of(
                "error", "Failed to bulk unblock users: " + e.getMessage()
            ));
        }
    }
    
    /**
     * Check if user is blocked
     */
    @GetMapping("/check/{targetUsername}")
    public ResponseEntity<?> isUserBlocked(@PathVariable String targetUsername, HttpSession session) {
        try {
            String username = getCurrentUsername(session);
            boolean isBlocked = blockService.isUserBlocked(username, targetUsername);
            
            return ResponseEntity.ok(Map.of(
                "isBlocked", isBlocked,
                "targetUser", targetUsername
            ));
            
        } catch (Exception e) {
            logger.error("Error checking if user is blocked: {}", e.getMessage());
            return ResponseEntity.status(500).body(Map.of(
                "error", "Failed to check block status: " + e.getMessage()
            ));
        }
    }
    
    private String getCurrentUsername(HttpSession session) {
        String username = (String) session.getAttribute("username");
        if (username == null) {
            throw new RuntimeException("User not authenticated");
        }
        return username;
    }
}
