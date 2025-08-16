package com.anuj.redditmessagemanager.controller;

import com.anuj.redditmessagemanager.dto.UserDto;
import com.anuj.redditmessagemanager.entity.User;
import com.anuj.redditmessagemanager.service.UserService;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import jakarta.servlet.http.HttpSession;
import java.util.List;
import java.util.Map;

@RestController
@RequestMapping("/api/user")
public class UserController {
    
    private static final Logger logger = LoggerFactory.getLogger(UserController.class);
    
    @Autowired
    private UserService userService;
    
    /**
     * Get current user profile
     */
    @GetMapping("/profile")
    public ResponseEntity<?> getUserProfile(HttpSession session) {
        try {
            User user = getCurrentUser(session);
            if (user == null) {
                return ResponseEntity.status(HttpStatus.UNAUTHORIZED)
                    .body(Map.of("error", "User not authenticated"));
            }
            
            UserDto userDto = userService.convertToDto(user);
            
            return ResponseEntity.ok(userDto);
            
        } catch (Exception e) {
            logger.error("Error getting user profile: {}", e.getMessage());
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
                .body(Map.of("error", "Failed to retrieve user profile: " + e.getMessage()));
        }
    }
    
    /**
     * Get user statistics
     */
    @GetMapping("/stats")
    public ResponseEntity<?> getUserStatistics(HttpSession session) {
        try {
            User user = getCurrentUser(session);
            if (user == null) {
                return ResponseEntity.status(HttpStatus.UNAUTHORIZED)
                    .body(Map.of("error", "User not authenticated"));
            }
            
            UserDto stats = userService.getUserStatistics(user.getRedditUsername());
            
            return ResponseEntity.ok(Map.of(
                "statistics", stats,
                "username", user.getRedditUsername()
            ));
            
        } catch (Exception e) {
            logger.error("Error getting user statistics: {}", e.getMessage());
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
                .body(Map.of("error", "Failed to retrieve user statistics: " + e.getMessage()));
        }
    }
    
    /**
     * Update user profile (limited fields)
     */
    @PutMapping("/profile")
    public ResponseEntity<?> updateUserProfile(@RequestBody Map<String, Object> updates,
                                              HttpSession session) {
        try {
            User user = getCurrentUser(session);
            if (user == null) {
                return ResponseEntity.status(HttpStatus.UNAUTHORIZED)
                    .body(Map.of("error", "User not authenticated"));
            }
            
            // Only allow updating non-sensitive fields
            if (updates.containsKey("isActive")) {
                user.setIsActive((Boolean) updates.get("isActive"));
            }
            
            User updatedUser = userService.save(user);
            UserDto userDto = userService.convertToDto(updatedUser);
            
            logger.info("User profile updated: {}", user.getRedditUsername());
            
            return ResponseEntity.ok(Map.of(
                "success", true,
                "message", "Profile updated successfully",
                "user", userDto
            ));
            
        } catch (Exception e) {
            logger.error("Error updating user profile: {}", e.getMessage());
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
                .body(Map.of("error", "Failed to update profile: " + e.getMessage()));
        }
    }
    
    /**
     * Deactivate user account
     */
    @PostMapping("/deactivate")
    public ResponseEntity<?> deactivateAccount(HttpSession session) {
        try {
            User user = getCurrentUser(session);
            if (user == null) {
                return ResponseEntity.status(HttpStatus.UNAUTHORIZED)
                    .body(Map.of("error", "User not authenticated"));
            }
            
            userService.deactivateUser(user.getId());
            session.invalidate(); // Log out user
            
            logger.info("User account deactivated: {}", user.getRedditUsername());
            
            return ResponseEntity.ok(Map.of(
                "success", true,
                "message", "Account deactivated successfully"
            ));
            
        } catch (Exception e) {
            logger.error("Error deactivating user account: {}", e.getMessage());
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
                .body(Map.of("error", "Failed to deactivate account: " + e.getMessage()));
        }
    }
    
    /**
     * Delete user account and all data
     */
    @DeleteMapping("/account")
    public ResponseEntity<?> deleteAccount(@RequestParam(required = true) String confirmation,
                                          HttpSession session) {
        try {
            if (!"DELETE_MY_ACCOUNT".equals(confirmation)) {
                return ResponseEntity.badRequest()
                    .body(Map.of("error", "Invalid confirmation. Please type 'DELETE_MY_ACCOUNT'"));
            }
            
            User user = getCurrentUser(session);
            if (user == null) {
                return ResponseEntity.status(HttpStatus.UNAUTHORIZED)
                    .body(Map.of("error", "User not authenticated"));
            }
            
            String username = user.getRedditUsername();
            userService.deleteUser(user.getId());
            session.invalidate(); // Log out user
            
            logger.info("User account deleted: {}", username);
            
            return ResponseEntity.ok(Map.of(
                "success", true,
                "message", "Account and all data deleted successfully"
            ));
            
        } catch (Exception e) {
            logger.error("Error deleting user account: {}", e.getMessage());
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
                .body(Map.of("error", "Failed to delete account: " + e.getMessage()));
        }
    }
    
    /**
     * Get all active users (admin only - for demonstration)
     */
    @GetMapping("/all")
    public ResponseEntity<?> getAllUsers(HttpSession session) {
        try {
            User user = getCurrentUser(session);
            if (user == null) {
                return ResponseEntity.status(HttpStatus.UNAUTHORIZED)
                    .body(Map.of("error", "User not authenticated"));
            }
            
            // Simple admin check - in real app, you'd have proper role-based access
            if (!"admin".equals(user.getRedditUsername())) {
                return ResponseEntity.status(HttpStatus.FORBIDDEN)
                    .body(Map.of("error", "Admin access required"));
            }
            
            List<User> users = userService.findAllActiveUsers();
            List<UserDto> userDtos = users.stream()
                .map(userService::convertToDto)
                .toList();
            
            return ResponseEntity.ok(Map.of(
                "users", userDtos,
                "count", userDtos.size()
            ));
            
        } catch (Exception e) {
            logger.error("Error getting all users: {}", e.getMessage());
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
                .body(Map.of("error", "Failed to retrieve users: " + e.getMessage()));
        }
    }
    
    /**
     * Cleanup inactive users (admin only)
     */
    @DeleteMapping("/cleanup")
    public ResponseEntity<?> cleanupInactiveUsers(@RequestParam(defaultValue = "90") int daysInactive,
                                                 HttpSession session) {
        try {
            User user = getCurrentUser(session);
            if (user == null) {
                return ResponseEntity.status(HttpStatus.UNAUTHORIZED)
                    .body(Map.of("error", "User not authenticated"));
            }
            
            // Simple admin check
            if (!"admin".equals(user.getRedditUsername())) {
                return ResponseEntity.status(HttpStatus.FORBIDDEN)
                    .body(Map.of("error", "Admin access required"));
            }
            
            int deletedCount = userService.cleanupInactiveUsers(daysInactive);
            
            return ResponseEntity.ok(Map.of(
                "success", true,
                "deletedCount", deletedCount,
                "message", "Cleaned up " + deletedCount + " inactive users"
            ));
            
        } catch (Exception e) {
            logger.error("Error cleaning up inactive users: {}", e.getMessage());
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
                .body(Map.of("error", "Failed to cleanup inactive users: " + e.getMessage()));
        }
    }
    
    /**
     * Helper method to get current user from session
     */
    private User getCurrentUser(HttpSession session) {
        Long userId = (Long) session.getAttribute("user_id");
        if (userId != null) {
            return userService.findById(userId);
        }
        return null;
    }
}
