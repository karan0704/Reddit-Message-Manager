package com.anuj.redditmessagemanager.controller;

import com.anuj.redditmessagemanager.dto.ChatDto;
import com.anuj.redditmessagemanager.dto.MessageDto;
import com.anuj.redditmessagemanager.dto.BulkActionDto;
import com.anuj.redditmessagemanager.entity.User;
import com.anuj.redditmessagemanager.service.ChatService;
import com.anuj.redditmessagemanager.service.MessageService;
import com.anuj.redditmessagemanager.service.UserService;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import jakarta.servlet.http.HttpSession;
import java.util.List;
import java.util.Map;

@RestController
@RequestMapping("/api/chat")
public class ChatController {
    
    private static final Logger logger = LoggerFactory.getLogger(ChatController.class);
    
    @Autowired
    private ChatService chatService;
    
    @Autowired
    private MessageService messageService;
    
    @Autowired
    private UserService userService;
    
    /**
     * Get all chats for current user
     */
    @GetMapping("/list")
    public ResponseEntity<?> getUserChats(
            @RequestParam(defaultValue = "false") boolean onlyPinned,
            @RequestParam(defaultValue = "false") boolean onlyUnread,
            HttpSession session) {
        try {
            String username = getCurrentUsername(session);
            List<ChatDto> chats;
            
            if (onlyPinned) {
                chats = chatService.getPinnedChats(username);
            } else if (onlyUnread) {
                chats = chatService.getChatsWithUnreadMessages(username);
            } else {
                chats = chatService.getUserChats(username);
            }
            
            return ResponseEntity.ok(Map.of(
                "chats", chats,
                "count", chats.size()
            ));
            
        } catch (Exception e) {
            logger.error("Error getting user chats: {}", e.getMessage());
            return ResponseEntity.status(500).body(Map.of(
                "error", "Failed to get chats: " + e.getMessage()
            ));
        }
    }
    
    /**
     * Get or create chat with another user
     */
    @PostMapping("/start")
    public ResponseEntity<?> startChat(@RequestBody Map<String, String> request, HttpSession session) {
        try {
            String username = getCurrentUsername(session);
            String otherUsername = request.get("otherUsername");
            
            if (otherUsername == null || otherUsername.equals(username)) {
                return ResponseEntity.badRequest().body(Map.of(
                    "error", "Invalid username"
                ));
            }
            
            // Check if other user exists and is not blocked
            User otherUser = userService.findByUsername(otherUsername);
            if (otherUser == null) {
                return ResponseEntity.badRequest().body(Map.of(
                    "error", "User not found"
                ));
            }
            
            ChatDto chat = chatService.getOrCreateChat(username, otherUsername);
            
            return ResponseEntity.ok(Map.of(
                "success", true,
                "chat", chat
            ));
            
        } catch (Exception e) {
            logger.error("Error starting chat: {}", e.getMessage());
            return ResponseEntity.status(500).body(Map.of(
                "error", "Failed to start chat: " + e.getMessage()
            ));
        }
    }
    
    /**
     * Get messages for a specific chat
     */
    @GetMapping("/{chatId}/messages")
    public ResponseEntity<?> getChatMessages(
            @PathVariable Long chatId, 
            @RequestParam(defaultValue = "0") int page,
            @RequestParam(defaultValue = "50") int size,
            HttpSession session) {
        try {
            String username = getCurrentUsername(session);
            List<MessageDto> messages = messageService.getChatMessages(chatId, username, page, size);
            
            // Mark messages as read when fetched
            chatService.markChatAsRead(chatId, username);
            
            return ResponseEntity.ok(Map.of(
                "messages", messages,
                "count", messages.size(),
                "page", page,
                "size", size
            ));
            
        } catch (Exception e) {
            logger.error("Error getting chat messages: {}", e.getMessage());
            return ResponseEntity.status(500).body(Map.of(
                "error", "Failed to get messages: " + e.getMessage()
            ));
        }
    }
    
    /**
     * Send message
     */
    @PostMapping("/{chatId}/send")
    public ResponseEntity<?> sendMessage(
            @PathVariable Long chatId,
            @RequestBody MessageDto messageDto,
            HttpSession session) {
        try {
            String username = getCurrentUsername(session);
            MessageDto sentMessage = messageService.sendMessage(chatId, username, messageDto);
            
            return ResponseEntity.ok(Map.of(
                "success", true,
                "message", sentMessage
            ));
            
        } catch (Exception e) {
            logger.error("Error sending message: {}", e.getMessage());
            return ResponseEntity.status(500).body(Map.of(
                "error", "Failed to send message: " + e.getMessage()
            ));
        }
    }
    
    /**
     * Pin/Unpin chat
     */
    @PostMapping("/{chatId}/pin")
    public ResponseEntity<?> togglePinChat(@PathVariable Long chatId, HttpSession session) {
        try {
            String username = getCurrentUsername(session);
            boolean isPinned = chatService.togglePinChat(chatId, username);
            
            return ResponseEntity.ok(Map.of(
                "success", true,
                "isPinned", isPinned
            ));
            
        } catch (Exception e) {
            logger.error("Error toggling pin status: {}", e.getMessage());
            return ResponseEntity.status(500).body(Map.of(
                "error", "Failed to toggle pin status: " + e.getMessage()
            ));
        }
    }
    
    /**
     * Archive/Unarchive chat
     */
    @PostMapping("/{chatId}/archive")
    public ResponseEntity<?> toggleArchiveChat(@PathVariable Long chatId, HttpSession session) {
        try {
            String username = getCurrentUsername(session);
            boolean isArchived = chatService.toggleArchiveChat(chatId, username);
            
            return ResponseEntity.ok(Map.of(
                "success", true,
                "isArchived", isArchived
            ));
            
        } catch (Exception e) {
            logger.error("Error toggling archive status: {}", e.getMessage());
            return ResponseEntity.status(500).body(Map.of(
                "error", "Failed to toggle archive status: " + e.getMessage()
            ));
        }
    }
    
    /**
     * Bulk operations on chats
     */
    @PostMapping("/bulk-action")
    public ResponseEntity<?> bulkChatAction(@RequestBody BulkActionDto bulkAction, HttpSession session) {
        try {
            String username = getCurrentUsername(session);
            int processedCount = chatService.processBulkAction(bulkAction, username);
            
            return ResponseEntity.ok(Map.of(
                "success", true,
                "processedCount", processedCount,
                "action", bulkAction.getActionType()
            ));
            
        } catch (Exception e) {
            logger.error("Error processing bulk action: {}", e.getMessage());
            return ResponseEntity.status(500).body(Map.of(
                "error", "Failed to process bulk action: " + e.getMessage()
            ));
        }
    }
    
    /**
     * Get chat statistics
     */
    @GetMapping("/stats")
    public ResponseEntity<?> getChatStatistics(HttpSession session) {
        try {
            String username = getCurrentUsername(session);
            Map<String, Object> stats = chatService.getChatStatistics(username);
            
            return ResponseEntity.ok(stats);
            
        } catch (Exception e) {
            logger.error("Error getting chat statistics: {}", e.getMessage());
            return ResponseEntity.status(500).body(Map.of(
                "error", "Failed to get statistics: " + e.getMessage()
            ));
        }
    }
    
    /**
     * Toggle image visibility in chat
     */
    @PostMapping("/{chatId}/toggle-images")
    public ResponseEntity<?> toggleImageVisibility(@PathVariable Long chatId, HttpSession session) {
        try {
            String username = getCurrentUsername(session);
            boolean imagesVisible = messageService.toggleImageVisibility(chatId, username);
            
            return ResponseEntity.ok(Map.of(
                "success", true,
                "imagesVisible", imagesVisible
            ));
            
        } catch (Exception e) {
            logger.error("Error toggling image visibility: {}", e.getMessage());
            return ResponseEntity.status(500).body(Map.of(
                "error", "Failed to toggle image visibility: " + e.getMessage()
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
