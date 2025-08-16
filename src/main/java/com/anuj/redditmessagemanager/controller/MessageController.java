package com.anuj.redditmessagemanager.controller;

import com.anuj.redditmessagemanager.dto.RedditMessageDto;
import com.anuj.redditmessagemanager.entity.RedditMessage.MessageType;
import com.anuj.redditmessagemanager.entity.User;
import com.anuj.redditmessagemanager.service.RedditMessageService;
import com.anuj.redditmessagemanager.service.UserService;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.domain.Page;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import jakarta.servlet.http.HttpSession;
import java.time.LocalDateTime;
import java.util.List;
import java.util.Map;

@RestController
@RequestMapping("/api/messages")
public class MessageController {
    
    private static final Logger logger = LoggerFactory.getLogger(MessageController.class);
    
    @Autowired
    private RedditMessageService messageService;
    
    @Autowired
    private UserService userService;
    
    /**
     * Get messages by type (inbox, sent, unread)
     */
    @GetMapping("/{type}")
    public ResponseEntity<?> getMessages(@PathVariable String type, 
                                        @RequestParam(defaultValue = "false") boolean refresh,
                                        HttpSession session) {
        try {
            User user = getCurrentUser(session);
            if (user == null) {
                return ResponseEntity.status(HttpStatus.UNAUTHORIZED)
                    .body(Map.of("error", "User not authenticated"));
            }
            
            MessageType messageType = parseMessageType(type);
            if (messageType == null) {
                return ResponseEntity.badRequest()
                    .body(Map.of("error", "Invalid message type: " + type));
            }
            
            List<RedditMessageDto> messages;
            
            if (refresh) {
                // Fetch fresh messages from Reddit API
                messages = messageService.fetchAndStoreMessages(user, messageType);
                logger.info("Fetched fresh {} messages for user: {}", type, user.getRedditUsername());
            } else {
                // Get stored messages from database
                messages = messageService.getMessagesByType(user, messageType);
                logger.info("Retrieved {} stored {} messages for user: {}", 
                    messages.size(), type, user.getRedditUsername());
            }
            
            return ResponseEntity.ok(Map.of(
                "messages", messages,
                "count", messages.size(),
                "type", type,
                "refreshed", refresh
            ));
            
        } catch (Exception e) {
            logger.error("Error getting {} messages: {}", type, e.getMessage());
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
                .body(Map.of("error", "Failed to retrieve messages: " + e.getMessage()));
        }
    }
    
    /**
     * Get all messages with pagination
     */
    @GetMapping("/all")
    public ResponseEntity<?> getAllMessages(@RequestParam(defaultValue = "0") int page,
                                           @RequestParam(defaultValue = "20") int size,
                                           HttpSession session) {
        try {
            User user = getCurrentUser(session);
            if (user == null) {
                return ResponseEntity.status(HttpStatus.UNAUTHORIZED)
                    .body(Map.of("error", "User not authenticated"));
            }
            
            Page<RedditMessageDto> messagePage = messageService.getAllMessages(user, page, size);
            
            return ResponseEntity.ok(Map.of(
                "messages", messagePage.getContent(),
                "totalElements", messagePage.getTotalElements(),
                "totalPages", messagePage.getTotalPages(),
                "currentPage", page,
                "size", size,
                "hasNext", messagePage.hasNext(),
                "hasPrevious", messagePage.hasPrevious()
            ));
            
        } catch (Exception e) {
            logger.error("Error getting all messages: {}", e.getMessage());
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
                .body(Map.of("error", "Failed to retrieve messages: " + e.getMessage()));
        }
    }
    
    /**
     * Get unread messages
     */
    @GetMapping("/unread")
    public ResponseEntity<?> getUnreadMessages(HttpSession session) {
        try {
            User user = getCurrentUser(session);
            if (user == null) {
                return ResponseEntity.status(HttpStatus.UNAUTHORIZED)
                    .body(Map.of("error", "User not authenticated"));
            }
            
            List<RedditMessageDto> messages = messageService.getUnreadMessages(user);
            
            return ResponseEntity.ok(Map.of(
                "messages", messages,
                "count", messages.size()
            ));
            
        } catch (Exception e) {
            logger.error("Error getting unread messages: {}", e.getMessage());
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
                .body(Map.of("error", "Failed to retrieve unread messages: " + e.getMessage()));
        }
    }
    
    /**
     * Mark message as read
     */
    @PostMapping("/{messageId}/read")
    public ResponseEntity<?> markMessageAsRead(@PathVariable Long messageId, HttpSession session) {
        try {
            User user = getCurrentUser(session);
            if (user == null) {
                return ResponseEntity.status(HttpStatus.UNAUTHORIZED)
                    .body(Map.of("error", "User not authenticated"));
            }
            
            messageService.markMessageAsRead(user, messageId);
            
            return ResponseEntity.ok(Map.of(
                "success", true,
                "message", "Message marked as read",
                "messageId", messageId
            ));
            
        } catch (Exception e) {
            logger.error("Error marking message as read: {}", e.getMessage());
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
                .body(Map.of("error", "Failed to mark message as read: " + e.getMessage()));
        }
    }
    
    /**
     * Mark all messages as read
     */
    @PostMapping("/read-all")
    public ResponseEntity<?> markAllMessagesAsRead(HttpSession session) {
        try {
            User user = getCurrentUser(session);
            if (user == null) {
                return ResponseEntity.status(HttpStatus.UNAUTHORIZED)
                    .body(Map.of("error", "User not authenticated"));
            }
            
            messageService.markAllMessagesAsRead(user);
            
            return ResponseEntity.ok(Map.of(
                "success", true,
                "message", "All messages marked as read"
            ));
            
        } catch (Exception e) {
            logger.error("Error marking all messages as read: {}", e.getMessage());
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
                .body(Map.of("error", "Failed to mark all messages as read: " + e.getMessage()));
        }
    }
    
    /**
     * Get message statistics
     */
    @GetMapping("/stats")
    public ResponseEntity<?> getMessageStatistics(HttpSession session) {
        try {
            User user = getCurrentUser(session);
            if (user == null) {
                return ResponseEntity.status(HttpStatus.UNAUTHORIZED)
                    .body(Map.of("error", "User not authenticated"));
            }
            
            RedditMessageDto stats = messageService.getMessageStatistics(user);
            
            return ResponseEntity.ok(Map.of(
                "statistics", stats,
                "timestamp", LocalDateTime.now()
            ));
            
        } catch (Exception e) {
            logger.error("Error getting message statistics: {}", e.getMessage());
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
                .body(Map.of("error", "Failed to retrieve statistics: " + e.getMessage()));
        }
    }
    
    /**
     * Delete old messages
     */
    @DeleteMapping("/old")
    public ResponseEntity<?> deleteOldMessages(@RequestParam(defaultValue = "30") int daysOld,
                                              HttpSession session) {
        try {
            User user = getCurrentUser(session);
            if (user == null) {
                return ResponseEntity.status(HttpStatus.UNAUTHORIZED)
                    .body(Map.of("error", "User not authenticated"));
            }
            
            int deletedCount = messageService.deleteOldMessages(user, daysOld);
            
            return ResponseEntity.ok(Map.of(
                "success", true,
                "deletedCount", deletedCount,
                "message", "Deleted " + deletedCount + " old messages"
            ));
            
        } catch (Exception e) {
            logger.error("Error deleting old messages: {}", e.getMessage());
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
                .body(Map.of("error", "Failed to delete old messages: " + e.getMessage()));
        }
    }
    
    /**
     * Get messages by date range
     */
    @GetMapping("/date-range")
    public ResponseEntity<?> getMessagesByDateRange(@RequestParam String startDate,
                                                   @RequestParam String endDate,
                                                   HttpSession session) {
        try {
            User user = getCurrentUser(session);
            if (user == null) {
                return ResponseEntity.status(HttpStatus.UNAUTHORIZED)
                    .body(Map.of("error", "User not authenticated"));
            }
            
            LocalDateTime start = LocalDateTime.parse(startDate + "T00:00:00");
            LocalDateTime end = LocalDateTime.parse(endDate + "T23:59:59");
            
            List<RedditMessageDto> messages = messageService.getMessagesByDateRange(user, start, end);
            
            return ResponseEntity.ok(Map.of(
                "messages", messages,
                "count", messages.size(),
                "startDate", startDate,
                "endDate", endDate
            ));
            
        } catch (Exception e) {
            logger.error("Error getting messages by date range: {}", e.getMessage());
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
                .body(Map.of("error", "Failed to retrieve messages by date range: " + e.getMessage()));
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
    
    /**
     * Helper method to parse message type
     */
    private MessageType parseMessageType(String type) {
        return switch (type.toLowerCase()) {
            case "inbox" -> MessageType.INBOX;
            case "sent" -> MessageType.SENT;
            case "unread" -> MessageType.UNREAD;
            default -> null;
        };
    }
}
