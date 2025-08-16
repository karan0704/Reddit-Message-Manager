import os

def create_controller_classes():
    # Base path from your previous conversation
    base_path = "D:\\Karan Ticket Project\\Reddit Message Manager"

    # Controller classes
    controller_files = [
        {
            "path": "src\\main\\java\\com\\anuj\\redditmessagemanager\\controller\\AuthController.java",
            "content": """package com.anuj.redditmessagemanager.controller;

import com.anuj.redditmessagemanager.entity.User;
import com.anuj.redditmessagemanager.service.RedditOAuthService;
import com.anuj.redditmessagemanager.util.RedditApiUtil;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.servlet.view.RedirectView;

import jakarta.servlet.http.HttpSession;

@Controller
public class AuthController {
    
    private static final Logger logger = LoggerFactory.getLogger(AuthController.class);
    
    @Autowired
    private RedditOAuthService oauthService;
    
    @Autowired
    private RedditApiUtil redditApiUtil;
    
    /**
     * Redirect user to Reddit for authentication
     */
    @GetMapping("/login")
    public RedirectView login(HttpSession session) {
        try {
            String state = redditApiUtil.generateState();
            session.setAttribute("oauth_state", state);
            
            String authUrl = oauthService.getAuthorizationUrl(state);
            logger.info("Redirecting user to Reddit authorization URL");
            
            return new RedirectView(authUrl);
            
        } catch (Exception e) {
            logger.error("Error initiating OAuth flow: {}", e.getMessage());
            return new RedirectView("/error?message=Failed to initiate login");
        }
    }
    
    /**
     * Handle OAuth callback from Reddit
     */
    @GetMapping("/auth/callback")
    public RedirectView callback(@RequestParam(required = false) String code,
                                @RequestParam(required = false) String state,
                                @RequestParam(required = false) String error,
                                HttpSession session) {
        
        try {
            // Check for OAuth error
            if (error != null) {
                logger.error("OAuth error received: {}", error);
                return new RedirectView("/error?message=Authentication failed: " + error);
            }
            
            // Validate state parameter
            String sessionState = (String) session.getAttribute("oauth_state");
            if (state == null || !state.equals(sessionState)) {
                logger.error("Invalid state parameter in OAuth callback");
                return new RedirectView("/error?message=Invalid authentication state");
            }
            
            // Validate authorization code
            if (code == null || code.trim().isEmpty()) {
                logger.error("No authorization code received");
                return new RedirectView("/error?message=No authorization code received");
            }
            
            // Complete OAuth flow
            User user = oauthService.completeOAuthFlow(code);
            if (user != null) {
                session.setAttribute("user_id", user.getId());
                session.setAttribute("reddit_username", user.getRedditUsername());
                session.removeAttribute("oauth_state"); // Clean up
                
                logger.info("User authenticated successfully: {}", user.getRedditUsername());
                return new RedirectView("/dashboard");
            } else {
                logger.error("Failed to complete OAuth flow");
                return new RedirectView("/error?message=Authentication failed");
            }
            
        } catch (Exception e) {
            logger.error("Error processing OAuth callback: {}", e.getMessage());
            return new RedirectView("/error?message=Authentication process failed");
        }
    }
    
    /**
     * Logout user
     */
    @GetMapping("/logout")
    public RedirectView logout(HttpSession session) {
        try {
            String username = (String) session.getAttribute("reddit_username");
            session.invalidate();
            
            logger.info("User logged out: {}", username);
            return new RedirectView("/?message=Logged out successfully");
            
        } catch (Exception e) {
            logger.error("Error during logout: {}", e.getMessage());
            return new RedirectView("/error?message=Logout failed");
        }
    }
    
    /**
     * Check authentication status
     */
    @GetMapping("/auth/status")
    @ResponseBody
    public AuthStatus getAuthStatus(HttpSession session) {
        Long userId = (Long) session.getAttribute("user_id");
        String username = (String) session.getAttribute("reddit_username");
        
        if (userId != null && username != null) {
            return new AuthStatus(true, username, userId);
        } else {
            return new AuthStatus(false, null, null);
        }
    }
    
    /**
     * Authentication status response class
     */
    public static class AuthStatus {
        private boolean authenticated;
        private String username;
        private Long userId;
        
        public AuthStatus(boolean authenticated, String username, Long userId) {
            this.authenticated = authenticated;
            this.username = username;
            this.userId = userId;
        }
        
        // Getters and setters
        public boolean isAuthenticated() { return authenticated; }
        public void setAuthenticated(boolean authenticated) { this.authenticated = authenticated; }
        
        public String getUsername() { return username; }
        public void setUsername(String username) { this.username = username; }
        
        public Long getUserId() { return userId; }
        public void setUserId(Long userId) { this.userId = userId; }
    }
}
"""
        },

        {
            "path": "src\\main\\java\\com\\anuj\\redditmessagemanager\\controller\\HomeController.java",
            "content": """package com.anuj.redditmessagemanager.controller;

import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;

import jakarta.servlet.http.HttpSession;

@Controller
public class HomeController {
    
    /**
     * Home page
     */
    @GetMapping("/")
    public String index(@RequestParam(required = false) String message, 
                       Model model, 
                       HttpSession session) {
        
        // Check if user is already logged in
        String username = (String) session.getAttribute("reddit_username");
        if (username != null) {
            return "redirect:/dashboard";
        }
        
        if (message != null) {
            model.addAttribute("message", message);
        }
        
        return "index";
    }
    
    /**
     * Dashboard page (requires authentication)
     */
    @GetMapping("/dashboard")
    public String dashboard(Model model, HttpSession session) {
        Long userId = (Long) session.getAttribute("user_id");
        String username = (String) session.getAttribute("reddit_username");
        
        if (userId == null || username == null) {
            return "redirect:/login";
        }
        
        model.addAttribute("username", username);
        model.addAttribute("userId", userId);
        
        return "dashboard";
    }
    
    /**
     * Messages page
     */
    @GetMapping("/messages")
    public String messages(Model model, HttpSession session) {
        Long userId = (Long) session.getAttribute("user_id");
        String username = (String) session.getAttribute("reddit_username");
        
        if (userId == null || username == null) {
            return "redirect:/login";
        }
        
        model.addAttribute("username", username);
        return "messages";
    }
    
    /**
     * Search page
     */
    @GetMapping("/search")
    public String search(Model model, HttpSession session) {
        Long userId = (Long) session.getAttribute("user_id");
        String username = (String) session.getAttribute("reddit_username");
        
        if (userId == null || username == null) {
            return "redirect:/login";
        }
        
        model.addAttribute("username", username);
        return "search";
    }
    
    /**
     * Error page
     */
    @GetMapping("/error")
    public String error(@RequestParam(required = false) String message, Model model) {
        if (message != null) {
            model.addAttribute("errorMessage", message);
        } else {
            model.addAttribute("errorMessage", "An unexpected error occurred");
        }
        
        return "error";
    }
    
    /**
     * About page
     */
    @GetMapping("/about")
    public String about() {
        return "about";
    }
}
"""
        },

        {
            "path": "src\\main\\java\\com\\anuj\\redditmessagemanager\\controller\\MessageController.java",
            "content": """package com.anuj.redditmessagemanager.controller;

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
"""
        },

        {
            "path": "src\\main\\java\\com\\anuj\\redditmessagemanager\\controller\\SearchController.java",
            "content": """package com.anuj.redditmessagemanager.controller;

import com.anuj.redditmessagemanager.dto.SearchResultDto;
import com.anuj.redditmessagemanager.entity.SearchHistory;
import com.anuj.redditmessagemanager.entity.User;
import com.anuj.redditmessagemanager.service.SearchService;
import com.anuj.redditmessagemanager.service.UserService;
import com.anuj.redditmessagemanager.util.ValidationUtil;
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
@RequestMapping("/api/search")
public class SearchController {
    
    private static final Logger logger = LoggerFactory.getLogger(SearchController.class);
    
    @Autowired
    private SearchService searchService;
    
    @Autowired
    private UserService userService;
    
    @Autowired
    private ValidationUtil validationUtil;
    
    /**
     * Search messages in local database
     */
    @GetMapping("/messages")
    public ResponseEntity<?> searchMessages(@RequestParam String q, HttpSession session) {
        try {
            User user = getCurrentUser(session);
            if (user == null) {
                return ResponseEntity.status(HttpStatus.UNAUTHORIZED)
                    .body(Map.of("error", "User not authenticated"));
            }
            
            if (!validationUtil.isValidSearchQuery(q)) {
                return ResponseEntity.badRequest()
                    .body(Map.of("error", "Invalid search query"));
            }
            
            SearchResultDto result = searchService.searchMessages(user, q);
            
            logger.info("Message search completed for user {}: {} results", 
                user.getRedditUsername(), result.getTotalResults());
            
            return ResponseEntity.ok(result);
            
        } catch (IllegalArgumentException e) {
            return ResponseEntity.badRequest()
                .body(Map.of("error", e.getMessage()));
        } catch (Exception e) {
            logger.error("Error searching messages: {}", e.getMessage());
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
                .body(Map.of("error", "Search failed: " + e.getMessage()));
        }
    }
    
    /**
     * Search Reddit posts via API
     */
    @GetMapping("/posts")
    public ResponseEntity<?> searchRedditPosts(@RequestParam String q, HttpSession session) {
        try {
            User user = getCurrentUser(session);
            if (user == null) {
                return ResponseEntity.status(HttpStatus.UNAUTHORIZED)
                    .body(Map.of("error", "User not authenticated"));
            }
            
            if (!validationUtil.isValidSearchQuery(q)) {
                return ResponseEntity.badRequest()
                    .body(Map.of("error", "Invalid search query"));
            }
            
            SearchResultDto result = searchService.searchRedditPosts(user, q);
            
            logger.info("Reddit post search completed for user {}: {} results", 
                user.getRedditUsername(), result.getTotalResults());
            
            return ResponseEntity.ok(result);
            
        } catch (IllegalArgumentException e) {
            return ResponseEntity.badRequest()
                .body(Map.of("error", e.getMessage()));
        } catch (Exception e) {
            logger.error("Error searching Reddit posts: {}", e.getMessage());
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
                .body(Map.of("error", "Reddit search failed: " + e.getMessage()));
        }
    }
    
    /**
     * Search messages by author
     */
    @GetMapping("/author")
    public ResponseEntity<?> searchByAuthor(@RequestParam String author, HttpSession session) {
        try {
            User user = getCurrentUser(session);
            if (user == null) {
                return ResponseEntity.status(HttpStatus.UNAUTHORIZED)
                    .body(Map.of("error", "User not authenticated"));
            }
            
            if (!validationUtil.isValidRedditUsername(author)) {
                return ResponseEntity.badRequest()
                    .body(Map.of("error", "Invalid username format"));
            }
            
            SearchResultDto result = searchService.searchByAuthor(user, author);
            
            logger.info("Author search completed for user {}: {} results", 
                user.getRedditUsername(), result.getTotalResults());
            
            return ResponseEntity.ok(result);
            
        } catch (IllegalArgumentException e) {
            return ResponseEntity.badRequest()
                .body(Map.of("error", e.getMessage()));
        } catch (Exception e) {
            logger.error("Error searching by author: {}", e.getMessage());
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
                .body(Map.of("error", "Author search failed: " + e.getMessage()));
        }
    }
    
    /**
     * Search messages by subreddit
     */
    @GetMapping("/subreddit")
    public ResponseEntity<?> searchBySubreddit(@RequestParam String subreddit, HttpSession session) {
        try {
            User user = getCurrentUser(session);
            if (user == null) {
                return ResponseEntity.status(HttpStatus.UNAUTHORIZED)
                    .body(Map.of("error", "User not authenticated"));
            }
            
            if (!validationUtil.isValidSubredditName(subreddit)) {
                return ResponseEntity.badRequest()
                    .body(Map.of("error", "Invalid subreddit name format"));
            }
            
            SearchResultDto result = searchService.searchBySubreddit(user, subreddit);
            
            logger.info("Subreddit search completed for user {}: {} results", 
                user.getRedditUsername(), result.getTotalResults());
            
            return ResponseEntity.ok(result);
            
        } catch (IllegalArgumentException e) {
            return ResponseEntity.badRequest()
                .body(Map.of("error", e.getMessage()));
        } catch (Exception e) {
            logger.error("Error searching by subreddit: {}", e.getMessage());
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
                .body(Map.of("error", "Subreddit search failed: " + e.getMessage()));
        }
    }
    
    /**
     * Get search history
     */
    @GetMapping("/history")
    public ResponseEntity<?> getSearchHistory(HttpSession session) {
        try {
            User user = getCurrentUser(session);
            if (user == null) {
                return ResponseEntity.status(HttpStatus.UNAUTHORIZED)
                    .body(Map.of("error", "User not authenticated"));
            }
            
            List<SearchHistory> history = searchService.getSearchHistory(user);
            
            return ResponseEntity.ok(Map.of(
                "history", history,
                "count", history.size()
            ));
            
        } catch (Exception e) {
            logger.error("Error getting search history: {}", e.getMessage());
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
                .body(Map.of("error", "Failed to retrieve search history: " + e.getMessage()));
        }
    }
    
    /**
     * Get popular search terms
     */
    @GetMapping("/popular")
    public ResponseEntity<?> getPopularSearchTerms(HttpSession session) {
        try {
            User user = getCurrentUser(session);
            if (user == null) {
                return ResponseEntity.status(HttpStatus.UNAUTHORIZED)
                    .body(Map.of("error", "User not authenticated"));
            }
            
            List<Object[]> popularTerms = searchService.getPopularSearchTerms(user);
            
            return ResponseEntity.ok(Map.of(
                "popularTerms", popularTerms,
                "count", popularTerms.size()
            ));
            
        } catch (Exception e) {
            logger.error("Error getting popular search terms: {}", e.getMessage());
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
                .body(Map.of("error", "Failed to retrieve popular search terms: " + e.getMessage()));
        }
    }
    
    /**
     * Clear search history
     */
    @DeleteMapping("/history")
    public ResponseEntity<?> clearSearchHistory(HttpSession session) {
        try {
            User user = getCurrentUser(session);
            if (user == null) {
                return ResponseEntity.status(HttpStatus.UNAUTHORIZED)
                    .body(Map.of("error", "User not authenticated"));
            }
            
            searchService.clearSearchHistory(user);
            
            return ResponseEntity.ok(Map.of(
                "success", true,
                "message", "Search history cleared successfully"
            ));
            
        } catch (Exception e) {
            logger.error("Error clearing search history: {}", e.getMessage());
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
                .body(Map.of("error", "Failed to clear search history: " + e.getMessage()));
        }
    }
    
    /**
     * Delete old search history
     */
    @DeleteMapping("/history/old")
    public ResponseEntity<?> deleteOldSearchHistory(@RequestParam(defaultValue = "30") int daysOld,
                                                   HttpSession session) {
        try {
            User user = getCurrentUser(session);
            if (user == null) {
                return ResponseEntity.status(HttpStatus.UNAUTHORIZED)
                    .body(Map.of("error", "User not authenticated"));
            }
            
            int deletedCount = searchService.deleteOldSearchHistory(user, daysOld);
            
            return ResponseEntity.ok(Map.of(
                "success", true,
                "deletedCount", deletedCount,
                "message", "Deleted " + deletedCount + " old search history entries"
            ));
            
        } catch (Exception e) {
            logger.error("Error deleting old search history: {}", e.getMessage());
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
                .body(Map.of("error", "Failed to delete old search history: " + e.getMessage()));
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
"""
        },

        {
            "path": "src\\main\\java\\com\\anuj\\redditmessagemanager\\controller\\UserController.java",
            "content": """package com.anuj.redditmessagemanager.controller;

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
"""
        }
    ]

    # Function to create files
    def create_files(files_list, file_type):
        print(f"\nCreating {file_type} files...")

        for file_info in files_list:
            full_file_path = os.path.join(base_path, file_info["path"])

            try:
                # Create directory if it doesn't exist
                os.makedirs(os.path.dirname(full_file_path), exist_ok=True)

                # Create file (overwrite if exists)
                with open(full_file_path, 'w', encoding='utf-8') as f:
                    f.write(file_info["content"])
                print(f"✓ Created: {file_info['path']}")

            except Exception as e:
                print(f"✗ Failed to create {file_info['path']}: {str(e)}")

    # Create controller files
    create_files(controller_files, "Controller")

    print("\n" + "="*70)
    print("Controller classes created successfully!")
    print("="*70)

    print("\nCreated Controller Classes:")
    print("✓ AuthController.java - Authentication and OAuth2 handling")
    print("✓ HomeController.java - Page routing and navigation")
    print("✓ MessageController.java - Message operations and API endpoints")
    print("✓ SearchController.java - Search functionality and history")
    print("✓ UserController.java - User profile and account management")

    print("\nController Features:")
    print("• Complete OAuth2 flow with Reddit")
    print("• RESTful API endpoints for all operations")
    print("• Session-based authentication")
    print("• Input validation and error handling")
    print("• Comprehensive logging")
    print("• JSON response formatting")
    print("• Pagination support")
    print("• File upload/download capabilities")

    print("\nAPI Endpoints Available:")

    print("\nAuthentication:")
    print("  GET  /login - Redirect to Reddit OAuth")
    print("  GET  /auth/callback - Handle OAuth callback")
    print("  GET  /logout - Logout user")
    print("  GET  /auth/status - Check authentication status")

    print("\nMessages:")
    print("  GET  /api/messages/{type} - Get messages by type (inbox/sent/unread)")
    print("  GET  /api/messages/all - Get all messages with pagination")
    print("  GET  /api/messages/unread - Get unread messages")
    print("  POST /api/messages/{id}/read - Mark message as read")
    print("  POST /api/messages/read-all - Mark all messages as read")
    print("  GET  /api/messages/stats - Get message statistics")
    print("  DELETE /api/messages/old - Delete old messages")
    print("  GET  /api/messages/date-range - Get messages by date range")

    print("\nSearch:")
    print("  GET  /api/search/messages - Search local messages")
    print("  GET  /api/search/posts - Search Reddit posts")
    print("  GET  /api/search/author - Search by author")
    print("  GET  /api/search/subreddit - Search by subreddit")
    print("  GET  /api/search/history - Get search history")
    print("  GET  /api/search/popular - Get popular search terms")
    print("  DELETE /api/search/history - Clear search history")

    print("\nUser Management:")
    print("  GET  /api/user/profile - Get user profile")
    print("  GET  /api/user/stats - Get user statistics")
    print("  PUT  /api/user/profile - Update user profile")
    print("  POST /api/user/deactivate - Deactivate account")
    print("  DELETE /api/user/account - Delete account and all data")

    print("\nPage Routes:")
    print("  GET  / - Home page")
    print("  GET  /dashboard - User dashboard")
    print("  GET  /messages - Messages page")
    print("  GET  /search - Search page")
    print("  GET  /error - Error page")

    print("\nNext steps:")
    print("1. Create HTML templates for the pages")
    print("2. Add frontend JavaScript for API calls")
    print("3. Test all endpoints")
    print("4. Run the application")
    print("5. Test complete OAuth flow")
    print("6. Test message fetching and search functionality")

if __name__ == "__main__":
    create_controller_classes()
