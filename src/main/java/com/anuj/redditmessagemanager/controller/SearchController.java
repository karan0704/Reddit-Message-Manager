package com.anuj.redditmessagemanager.controller;

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
