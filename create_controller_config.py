import os

def create_controller_and_config_classes():
    # Base path from your previous conversation
    base_path = "D:\\Karan Ticket Project\\Reddit Message Manager"

    # Configuration classes for the local chat application
    config_files = [
        {
            "path": "src\\main\\java\\com\\anuj\\redditmessagemanager\\config\\LocalAuthConfig.java",
            "content": """package com.anuj.redditmessagemanager.config;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.web.servlet.config.annotation.InterceptorRegistry;
import org.springframework.web.servlet.config.annotation.WebMvcConfigurer;

@Configuration
public class LocalAuthConfig implements WebMvcConfigurer {
    
    /**
     * Authentication interceptor for session-based local authentication
     */
    @Bean
    public LocalAuthInterceptor localAuthInterceptor() {
        return new LocalAuthInterceptor();
    }
    
    @Override
    public void addInterceptors(InterceptorRegistry registry) {
        registry.addInterceptor(localAuthInterceptor())
                .addPathPatterns("/api/**", "/dashboard", "/chat/**")
                .excludePathPatterns("/api/auth/**", "/login", "/", "/static/**");
    }
    
    /**
     * Session timeout configuration (24 hours)
     */
    @Bean
    public SessionConfig sessionConfig() {
        return new SessionConfig();
    }
    
    public static class SessionConfig {
        private final int sessionTimeoutSeconds = 86400; // 24 hours
        private final boolean rememberLastUser = true;
        
        public int getSessionTimeoutSeconds() {
            return sessionTimeoutSeconds;
        }
        
        public boolean isRememberLastUser() {
            return rememberLastUser;
        }
    }
    
    public static class LocalAuthInterceptor implements org.springframework.web.servlet.HandlerInterceptor {
        @Override
        public boolean preHandle(jakarta.servlet.http.HttpServletRequest request, 
                               jakarta.servlet.http.HttpServletResponse response, 
                               Object handler) throws Exception {
            
            String username = (String) request.getSession().getAttribute("username");
            if (username == null) {
                response.sendRedirect("/login");
                return false;
            }
            return true;
        }
    }
}
"""
        },

        {
            "path": "src\\main\\java\\com\\anuj\\redditmessagemanager\\config\\WebSocketConfig.java",
            "content": """package com.anuj.redditmessagemanager.config;

import com.anuj.redditmessagemanager.websocket.ChatWebSocketHandler;
import org.springframework.context.annotation.Configuration;
import org.springframework.web.socket.config.annotation.*;

@Configuration
@EnableWebSocket
public class WebSocketConfig implements WebSocketConfigurer {

    @Override
    public void registerWebSocketHandlers(WebSocketHandlerRegistry registry) {
        registry.addHandler(new ChatWebSocketHandler(), "/ws/chat")
                .setAllowedOrigins("*")
                .withSockJS();
    }
}
"""
        },

        {
            "path": "src\\main\\java\\com\\anuj\\redditmessagemanager\\config\\DatabaseConfig.java",
            "content": """package com.anuj.redditmessagemanager.config;

import com.zaxxer.hikari.HikariConfig;
import com.zaxxer.hikari.HikariDataSource;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.context.annotation.Primary;

import javax.sql.DataSource;

@Configuration
public class DatabaseConfig {
    
    @Value("${spring.datasource.url}")
    private String dbUrl;
    
    @Value("${spring.datasource.username}")
    private String dbUsername;
    
    @Value("${spring.datasource.password}")
    private String dbPassword;
    
    @Bean
    @Primary
    public DataSource dataSource() {
        HikariConfig config = new HikariConfig();
        config.setJdbcUrl(dbUrl);
        config.setUsername(dbUsername);
        config.setPassword(dbPassword);
        
        // Connection pool settings for chat application
        config.setMaximumPoolSize(50);
        config.setMinimumIdle(10);
        config.setConnectionTimeout(30000);
        config.setIdleTimeout(600000);
        config.setMaxLifetime(1800000);
        
        return new HikariDataSource(config);
    }
}
"""
        },

        {
            "path": "src\\main\\java\\com\\anuj\\redditmessagemanager\\config\\WebConfig.java",
            "content": """package com.anuj.redditmessagemanager.config;

import org.springframework.context.annotation.Configuration;
import org.springframework.web.servlet.config.annotation.*;

@Configuration
public class WebConfig implements WebMvcConfigurer {
    
    @Override
    public void addCorsMappings(CorsRegistry registry) {
        registry.addMapping("/api/**")
                .allowedOrigins("http://localhost:8080")
                .allowedMethods("GET", "POST", "PUT", "DELETE", "OPTIONS")
                .allowedHeaders("*")
                .allowCredentials(true);
    }
    
    @Override
    public void addResourceHandlers(ResourceHandlerRegistry registry) {
        registry.addResourceHandler("/static/**")
                .addResourceLocations("classpath:/static/")
                .setCachePeriod(3600);
        
        registry.addResourceHandler("/uploads/**")
                .addResourceLocations("file:./uploads/")
                .setCachePeriod(3600);
    }
    
    @Override
    public void addViewControllers(ViewControllerRegistry registry) {
        registry.addViewController("/").setViewName("index");
        registry.addViewController("/login").setViewName("login");
        registry.addViewController("/dashboard").setViewName("dashboard");
        registry.addViewController("/chat").setViewName("chat");
    }
}
"""
        }
    ]

    # Controller classes for the local chat application
    controller_files = [
        {
            "path": "src\\main\\java\\com\\anuj\\redditmessagemanager\\controller\\AuthController.java",
            "content": """package com.anuj.redditmessagemanager.controller;

import com.anuj.redditmessagemanager.dto.AuthDto;
import com.anuj.redditmessagemanager.dto.UserDto;
import com.anuj.redditmessagemanager.entity.User;
import com.anuj.redditmessagemanager.service.LocalAuthService;
import com.anuj.redditmessagemanager.service.UserService;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.*;

import jakarta.servlet.http.HttpSession;
import java.time.LocalDateTime;
import java.util.List;
import java.util.Map;

@Controller
@RequestMapping("/api/auth")
public class AuthController {
    
    private static final Logger logger = LoggerFactory.getLogger(AuthController.class);
    
    @Autowired
    private LocalAuthService authService;
    
    @Autowired
    private UserService userService;
    
    /**
     * Mock login with local authentication
     */
    @PostMapping("/login")
    @ResponseBody
    public ResponseEntity<?> login(@RequestBody AuthDto authDto, HttpSession session) {
        try {
            logger.info("Login attempt for username: {}", authDto.getUsername());
            
            User user = authService.authenticateUser(authDto.getUsername(), authDto.getPassword());
            
            if (user != null) {
                // Set session attributes
                session.setAttribute("username", user.getUsername());
                session.setAttribute("user_id", user.getId());
                session.setAttribute("display_name", user.getDisplayName());
                
                // Update user login info
                userService.updateUserLogin(user.getUsername(), authDto.getRememberMe());
                
                AuthDto response = new AuthDto();
                response.setUsername(user.getUsername());
                response.setDisplayName(user.getDisplayName());
                response.setIsAuthenticated(true);
                response.setLoginTime(LocalDateTime.now());
                response.setRememberMe(authDto.getRememberMe());
                
                logger.info("User authenticated successfully: {}", user.getUsername());
                return ResponseEntity.ok(Map.of(
                    "success", true,
                    "user", response,
                    "message", "Login successful"
                ));
            } else {
                return ResponseEntity.status(401).body(Map.of(
                    "success", false,
                    "message", "Invalid username or password"
                ));
            }
            
        } catch (Exception e) {
            logger.error("Login error: {}", e.getMessage());
            return ResponseEntity.status(500).body(Map.of(
                "success", false,
                "message", "Login failed: " + e.getMessage()
            ));
        }
    }
    
    /**
     * Quick login for remembered users
     */
    @PostMapping("/quick-login")
    @ResponseBody
    public ResponseEntity<?> quickLogin(@RequestBody Map<String, String> request, HttpSession session) {
        try {
            String username = request.get("username");
            
            User user = userService.findByUsername(username);
            if (user != null && user.getIsRemembered()) {
                session.setAttribute("username", user.getUsername());
                session.setAttribute("user_id", user.getId());
                session.setAttribute("display_name", user.getDisplayName());
                
                userService.updateUserLogin(user.getUsername(), true);
                
                logger.info("Quick login successful for: {}", username);
                return ResponseEntity.ok(Map.of(
                    "success", true,
                    "username", user.getUsername(),
                    "displayName", user.getDisplayName()
                ));
            } else {
                return ResponseEntity.status(401).body(Map.of(
                    "success", false,
                    "message", "Quick login not available"
                ));
            }
            
        } catch (Exception e) {
            logger.error("Quick login error: {}", e.getMessage());
            return ResponseEntity.status(500).body(Map.of(
                "success", false,
                "message", "Quick login failed"
            ));
        }
    }
    
    /**
     * Register new user (mock registration)
     */
    @PostMapping("/register")
    @ResponseBody
    public ResponseEntity<?> register(@RequestBody AuthDto authDto) {
        try {
            if (userService.existsByUsername(authDto.getUsername())) {
                return ResponseEntity.status(400).body(Map.of(
                    "success", false,
                    "message", "Username already exists"
                ));
            }
            
            User user = authService.createUser(authDto.getUsername(), authDto.getDisplayName(), 
                                             authDto.getEmail(), authDto.getPassword());
            
            if (user != null) {
                logger.info("User registered successfully: {}", user.getUsername());
                return ResponseEntity.ok(Map.of(
                    "success", true,
                    "message", "Registration successful",
                    "username", user.getUsername()
                ));
            } else {
                return ResponseEntity.status(500).body(Map.of(
                    "success", false,
                    "message", "Registration failed"
                ));
            }
            
        } catch (Exception e) {
            logger.error("Registration error: {}", e.getMessage());
            return ResponseEntity.status(500).body(Map.of(
                "success", false,
                "message", "Registration failed: " + e.getMessage()
            ));
        }
    }
    
    /**
     * Logout user
     */
    @PostMapping("/logout")
    @ResponseBody
    public ResponseEntity<?> logout(HttpSession session) {
        try {
            String username = (String) session.getAttribute("username");
            
            if (username != null) {
                userService.updateUserOnlineStatus(username, false);
                session.invalidate();
                
                logger.info("User logged out: {}", username);
                return ResponseEntity.ok(Map.of(
                    "success", true,
                    "message", "Logout successful"
                ));
            }
            
            return ResponseEntity.ok(Map.of("success", true));
            
        } catch (Exception e) {
            logger.error("Logout error: {}", e.getMessage());
            return ResponseEntity.status(500).body(Map.of(
                "success", false,
                "message", "Logout failed"
            ));
        }
    }
    
    /**
     * Get authentication status
     */
    @GetMapping("/status")
    @ResponseBody
    public ResponseEntity<?> getAuthStatus(HttpSession session) {
        String username = (String) session.getAttribute("username");
        String displayName = (String) session.getAttribute("display_name");
        Long userId = (Long) session.getAttribute("user_id");
        
        if (username != null) {
            return ResponseEntity.ok(Map.of(
                "authenticated", true,
                "username", username,
                "displayName", displayName != null ? displayName : username,
                "userId", userId
            ));
        } else {
            return ResponseEntity.ok(Map.of(
                "authenticated", false
            ));
        }
    }
    
    /**
     * Get remembered users for quick login
     */
    @GetMapping("/remembered-users")
    @ResponseBody
    public ResponseEntity<?> getRememberedUsers() {
        try {
            List<UserDto> rememberedUsers = userService.getRememberedUsers();
            return ResponseEntity.ok(Map.of(
                "users", rememberedUsers
            ));
        } catch (Exception e) {
            logger.error("Error getting remembered users: {}", e.getMessage());
            return ResponseEntity.status(500).body(Map.of(
                "error", "Failed to get remembered users"
            ));
        }
    }
}
"""
        },

        {
            "path": "src\\main\\java\\com\\anuj\\redditmessagemanager\\controller\\ChatController.java",
            "content": """package com.anuj.redditmessagemanager.controller;

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
"""
        },

        {
            "path": "src\\main\\java\\com\\anuj\\redditmessagemanager\\controller\\SearchController.java",
            "content": """package com.anuj.redditmessagemanager.controller;

import com.anuj.redditmessagemanager.dto.SearchResultDto;
import com.anuj.redditmessagemanager.dto.FilterDto;
import com.anuj.redditmessagemanager.entity.SearchHistory;
import com.anuj.redditmessagemanager.service.SearchService;
import com.anuj.redditmessagemanager.service.UserService;
import com.anuj.redditmessagemanager.util.ValidationUtil;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
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
     * Search messages by content
     */
    @GetMapping("/messages")
    public ResponseEntity<?> searchMessages(
            @RequestParam String q,
            @RequestParam(required = false) Long chatId,
            HttpSession session) {
        try {
            String username = getCurrentUsername(session);
            
            if (!validationUtil.isValidSearchQuery(q)) {
                return ResponseEntity.badRequest().body(Map.of(
                    "error", "Invalid search query"
                ));
            }
            
            SearchResultDto result = searchService.searchMessages(username, q, chatId);
            
            return ResponseEntity.ok(result);
            
        } catch (Exception e) {
            logger.error("Error searching messages: {}", e.getMessage());
            return ResponseEntity.status(500).body(Map.of(
                "error", "Search failed: " + e.getMessage()
            ));
        }
    }
    
    /**
     * Search users for autocomplete
     */
    @GetMapping("/users")
    public ResponseEntity<?> searchUsers(@RequestParam String q, HttpSession session) {
        try {
            String username = getCurrentUsername(session);
            
            if (q.length() < 2) {
                return ResponseEntity.badRequest().body(Map.of(
                    "error", "Search query must be at least 2 characters"
                ));
            }
            
            SearchResultDto result = searchService.searchUsers(username, q);
            
            return ResponseEntity.ok(result);
            
        } catch (Exception e) {
            logger.error("Error searching users: {}", e.getMessage());
            return ResponseEntity.status(500).body(Map.of(
                "error", "User search failed: " + e.getMessage()
            ));
        }
    }
    
    /**
     * Search chats
     */
    @GetMapping("/chats")
    public ResponseEntity<?> searchChats(@RequestParam String q, HttpSession session) {
        try {
            String username = getCurrentUsername(session);
            
            if (!validationUtil.isValidSearchQuery(q)) {
                return ResponseEntity.badRequest().body(Map.of(
                    "error", "Invalid search query"
                ));
            }
            
            SearchResultDto result = searchService.searchChats(username, q);
            
            return ResponseEntity.ok(result);
            
        } catch (Exception e) {
            logger.error("Error searching chats: {}", e.getMessage());
            return ResponseEntity.status(500).body(Map.of(
                "error", "Chat search failed: " + e.getMessage()
            ));
        }
    }
    
    /**
     * Advanced search with filters
     */
    @PostMapping("/advanced")
    public ResponseEntity<?> advancedSearch(@RequestBody FilterDto filter, HttpSession session) {
        try {
            String username = getCurrentUsername(session);
            
            SearchResultDto result = searchService.advancedSearch(username, filter);
            
            return ResponseEntity.ok(result);
            
        } catch (Exception e) {
            logger.error("Error in advanced search: {}", e.getMessage());
            return ResponseEntity.status(500).body(Map.of(
                "error", "Advanced search failed: " + e.getMessage()
            ));
        }
    }
    
    /**
     * Get search history
     */
    @GetMapping("/history")
    public ResponseEntity<?> getSearchHistory(HttpSession session) {
        try {
            String username = getCurrentUsername(session);
            List<SearchHistory> history = searchService.getSearchHistory(username);
            
            return ResponseEntity.ok(Map.of(
                "history", history,
                "count", history.size()
            ));
            
        } catch (Exception e) {
            logger.error("Error getting search history: {}", e.getMessage());
            return ResponseEntity.status(500).body(Map.of(
                "error", "Failed to retrieve search history: " + e.getMessage()
            ));
        }
    }
    
    /**
     * Get autocomplete suggestions
     */
    @GetMapping("/suggestions")
    public ResponseEntity<?> getAutocompleteSuggestions(
            @RequestParam String q,
            @RequestParam(defaultValue = "all") String type,
            HttpSession session) {
        try {
            String username = getCurrentUsername(session);
            List<String> suggestions = searchService.getAutocompleteSuggestions(username, q, type);
            
            return ResponseEntity.ok(Map.of(
                "suggestions", suggestions,
                "query", q,
                "type", type
            ));
            
        } catch (Exception e) {
            logger.error("Error getting autocomplete suggestions: {}", e.getMessage());
            return ResponseEntity.status(500).body(Map.of(
                "error", "Failed to get suggestions: " + e.getMessage()
            ));
        }
    }
    
    /**
     * Clear search history
     */
    @DeleteMapping("/history")
    public ResponseEntity<?> clearSearchHistory(HttpSession session) {
        try {
            String username = getCurrentUsername(session);
            searchService.clearSearchHistory(username);
            
            return ResponseEntity.ok(Map.of(
                "success", true,
                "message", "Search history cleared"
            ));
            
        } catch (Exception e) {
            logger.error("Error clearing search history: {}", e.getMessage());
            return ResponseEntity.status(500).body(Map.of(
                "error", "Failed to clear search history: " + e.getMessage()
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
"""
        },

        {
            "path": "src\\main\\java\\com\\anuj\\redditmessagemanager\\controller\\BlockController.java",
            "content": """package com.anuj.redditmessagemanager.controller;

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
"""
        },

        {
            "path": "src\\main\\java\\com\\anuj\\redditmessagemanager\\controller\\ExportController.java",
            "content": """package com.anuj.redditmessagemanager.controller;

import com.anuj.redditmessagemanager.dto.ExportDto;
import com.anuj.redditmessagemanager.service.ExportService;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.core.io.Resource;
import org.springframework.http.HttpHeaders;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import jakarta.servlet.http.HttpSession;
import java.util.Map;

@RestController
@RequestMapping("/api/export")
public class ExportController {
    
    private static final Logger logger = LoggerFactory.getLogger(ExportController.class);
    
    @Autowired
    private ExportService exportService;
    
    /**
     * Export chats to file
     */
    @PostMapping("/chats")
    public ResponseEntity<?> exportChats(@RequestBody ExportDto exportRequest, HttpSession session) {
        try {
            String username = getCurrentUsername(session);
            ExportDto exportResult = exportService.exportChats(username, exportRequest);
            
            return ResponseEntity.ok(Map.of(
                "success", true,
                "export", exportResult,
                "message", "Export started successfully"
            ));
            
        } catch (Exception e) {
            logger.error("Error starting export: {}", e.getMessage());
            return ResponseEntity.status(500).body(Map.of(
                "error", "Export failed: " + e.getMessage()
            ));
        }
    }
    
    /**
     * Download exported file
     */
    @GetMapping("/download/{filename}")
    public ResponseEntity<Resource> downloadExportedFile(@PathVariable String filename, HttpSession session) {
        try {
            String username = getCurrentUsername(session);
            Resource file = exportService.getExportedFile(username, filename);
            
            return ResponseEntity.ok()
                    .contentType(MediaType.APPLICATION_OCTET_STREAM)
                    .header(HttpHeaders.CONTENT_DISPOSITION, "attachment; filename=\"" + filename + "\"")
                    .body(file);
                    
        } catch (Exception e) {
            logger.error("Error downloading file: {}", e.getMessage());
            return ResponseEntity.notFound().build();
        }
    }
    
    /**
     * Get export status
     */
    @GetMapping("/status/{exportId}")
    public ResponseEntity<?> getExportStatus(@PathVariable String exportId, HttpSession session) {
        try {
            String username = getCurrentUsername(session);
            ExportDto status = exportService.getExportStatus(username, exportId);
            
            return ResponseEntity.ok(status);
            
        } catch (Exception e) {
            logger.error("Error getting export status: {}", e.getMessage());
            return ResponseEntity.status(500).body(Map.of(
                "error", "Failed to get export status: " + e.getMessage()
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

    # Create configuration and controller files
    create_files(config_files, "Configuration")
    create_files(controller_files, "Controller")

    print("\n" + "="*70)
    print("Controller and Configuration classes created successfully!")
    print("="*70)

    print("\nCreated Configuration Classes:")
    print("✓ LocalAuthConfig.java - Local authentication with session management")
    print("✓ WebSocketConfig.java - WebSocket configuration for real-time chat")
    print("✓ DatabaseConfig.java - HikariCP connection pool configuration")
    print("✓ WebConfig.java - CORS, static resources, and view controllers")

    print("\nCreated Controller Classes:")
    print("✓ AuthController.java - Local authentication endpoints")
    print("✓ ChatController.java - Chat management and messaging")
    print("✓ SearchController.java - Search functionality with filters")
    print("✓ BlockController.java - User blocking/unblocking")
    print("✓ ExportController.java - Chat export functionality")

    print("\nController Features:")
    print("• Local authentication with 'remember me' functionality[1]")
    print("• Session-based authentication without external APIs[1]")
    print("• Real-time chat messaging via WebSocket")
    print("• Advanced search with autocomplete suggestions")
    print("• Bulk operations (delete, pin, block multiple items)")
    print("• User blocking/unblocking with bulk operations")
    print("• Chat export to multiple formats (TXT, JSON)")
    print("• Pin/unpin chats to top")
    print("• Archive/unarchive functionality")
    print("• Image visibility toggle")
    print("• Comprehensive error handling and logging[1]")

    print("\nAPI Endpoints Available:")

    print("\nAuthentication:")
    print("  POST /api/auth/login - Local login")
    print("  POST /api/auth/register - User registration")
    print("  POST /api/auth/quick-login - Quick login for remembered users")
    print("  POST /api/auth/logout - Logout")
    print("  GET  /api/auth/status - Check authentication status")
    print("  GET  /api/auth/remembered-users - Get remembered users list")

    print("\nChat Management:")
    print("  GET  /api/chat/list - Get user's chats")
    print("  POST /api/chat/start - Start new chat")
    print("  GET  /api/chat/{id}/messages - Get chat messages")
    print("  POST /api/chat/{id}/send - Send message")
    print("  POST /api/chat/{id}/pin - Pin/unpin chat")
    print("  POST /api/chat/bulk-action - Bulk operations")

    print("\nSearch & Filter:")
    print("  GET  /api/search/messages - Search messages")
    print("  GET  /api/search/users - Search users (autocomplete)")
    print("  GET  /api/search/chats - Search chats")
    print("  POST /api/search/advanced - Advanced search with filters")
    print("  GET  /api/search/history - Get search history")

    print("\nUser Management:")
    print("  POST /api/block/user - Block user")
    print("  DELETE /api/block/user/{username} - Unblock user")
    print("  GET  /api/block/list - Get blocked users")
    print("  POST /api/block/bulk-unblock - Bulk unblock users")

    print("\nExport:")
    print("  POST /api/export/chats - Export chats")
    print("  GET  /api/export/download/{filename} - Download exported file")
    print("  GET  /api/export/status/{id} - Get export status")

    print("\nNext steps:")
    print("1. Create the service classes to implement business logic")
    print("2. Create WebSocket handler for real-time messaging")
    print("3. Test all API endpoints")
    print("4. Create frontend templates")
    print("5. Test the complete authentication flow")

if __name__ == "__main__":
    create_controller_and_config_classes()