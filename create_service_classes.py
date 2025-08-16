import os

def create_service_classes():
    # Base path from your previous conversation
    base_path = "D:\\Karan Ticket Project\\Reddit Message Manager"

    # Service classes
    service_files = [
        {
            "path": "src\\main\\java\\com\\anuj\\redditmessagemanager\\service\\RedditOAuthService.java",
            "content": """package com.anuj.redditmessagemanager.service;

import com.anuj.redditmessagemanager.config.RedditConfig;
import com.anuj.redditmessagemanager.dto.RedditTokenResponse;
import com.anuj.redditmessagemanager.entity.User;
import com.anuj.redditmessagemanager.util.RedditApiUtil;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.*;
import org.springframework.stereotype.Service;
import org.springframework.util.LinkedMultiValueMap;
import org.springframework.util.MultiValueMap;
import org.springframework.web.client.RestTemplate;

import java.time.LocalDateTime;
import java.util.Map;

@Service
public class RedditOAuthService {
    
    private static final Logger logger = LoggerFactory.getLogger(RedditOAuthService.class);
    
    @Autowired
    private RedditConfig redditConfig;
    
    @Autowired
    private RestTemplate restTemplate;
    
    @Autowired
    private RedditApiUtil redditApiUtil;
    
    @Autowired
    private UserService userService;
    
    /**
     * Generate authorization URL for Reddit OAuth
     */
    public String getAuthorizationUrl(String state) {
        return String.format(redditConfig.getAuthorizationUrl(), state);
    }
    
    /**
     * Exchange authorization code for access token
     */
    public RedditTokenResponse exchangeCodeForToken(String code) {
        try {
            HttpHeaders headers = new HttpHeaders();
            headers.setContentType(MediaType.APPLICATION_FORM_URLENCODED);
            headers.set("Authorization", redditApiUtil.createBasicAuthHeader(
                redditConfig.getClientId(), redditConfig.getClientSecret()));
            headers.set("User-Agent", "RedditMessageManager/1.0");
            
            MultiValueMap<String, String> body = new LinkedMultiValueMap<>();
            body.add("grant_type", "authorization_code");
            body.add("code", code);
            body.add("redirect_uri", redditConfig.getRedirectUri());
            
            HttpEntity<MultiValueMap<String, String>> request = new HttpEntity<>(body, headers);
            
            ResponseEntity<RedditTokenResponse> response = restTemplate.postForEntity(
                "https://www.reddit.com/api/v1/access_token", 
                request, 
                RedditTokenResponse.class
            );
            
            if (response.getStatusCode() == HttpStatus.OK) {
                logger.info("Successfully exchanged code for token");
                return response.getBody();
            } else {
                logger.error("Failed to exchange code for token. Status: {}", response.getStatusCode());
                return null;
            }
            
        } catch (Exception e) {
            logger.error("Error exchanging code for token: {}", e.getMessage());
            return null;
        }
    }
    
    /**
     * Refresh access token using refresh token
     */
    public RedditTokenResponse refreshAccessToken(String refreshToken) {
        try {
            HttpHeaders headers = new HttpHeaders();
            headers.setContentType(MediaType.APPLICATION_FORM_URLENCODED);
            headers.set("Authorization", redditApiUtil.createBasicAuthHeader(
                redditConfig.getClientId(), redditConfig.getClientSecret()));
            headers.set("User-Agent", "RedditMessageManager/1.0");
            
            MultiValueMap<String, String> body = new LinkedMultiValueMap<>();
            body.add("grant_type", "refresh_token");
            body.add("refresh_token", refreshToken);
            
            HttpEntity<MultiValueMap<String, String>> request = new HttpEntity<>(body, headers);
            
            ResponseEntity<RedditTokenResponse> response = restTemplate.postForEntity(
                "https://www.reddit.com/api/v1/access_token", 
                request, 
                RedditTokenResponse.class
            );
            
            if (response.getStatusCode() == HttpStatus.OK) {
                logger.info("Successfully refreshed access token");
                return response.getBody();
            } else {
                logger.error("Failed to refresh token. Status: {}", response.getStatusCode());
                return null;
            }
            
        } catch (Exception e) {
            logger.error("Error refreshing access token: {}", e.getMessage());
            return null;
        }
    }
    
    /**
     * Get Reddit user info using access token
     */
    @SuppressWarnings("unchecked")
    public Map<String, Object> getUserInfo(String accessToken) {
        try {
            HttpHeaders headers = new HttpHeaders();
            headers.set("Authorization", "Bearer " + accessToken);
            headers.set("User-Agent", "RedditMessageManager/1.0");
            
            HttpEntity<String> entity = new HttpEntity<>(headers);
            
            ResponseEntity<Map> response = restTemplate.exchange(
                "https://oauth.reddit.com/api/v1/me",
                HttpMethod.GET,
                entity,
                Map.class
            );
            
            if (response.getStatusCode() == HttpStatus.OK) {
                logger.info("Successfully retrieved user info");
                return response.getBody();
            } else {
                logger.error("Failed to get user info. Status: {}", response.getStatusCode());
                return null;
            }
            
        } catch (Exception e) {
            logger.error("Error getting user info: {}", e.getMessage());
            return null;
        }
    }
    
    /**
     * Complete OAuth process - exchange code and create/update user
     */
    public User completeOAuthFlow(String code) {
        try {
            // Exchange code for token
            RedditTokenResponse tokenResponse = exchangeCodeForToken(code);
            if (tokenResponse == null) {
                logger.error("Failed to get token response");
                return null;
            }
            
            // Get user info
            Map<String, Object> userInfo = getUserInfo(tokenResponse.getAccessToken());
            if (userInfo == null) {
                logger.error("Failed to get user info");
                return null;
            }
            
            String username = (String) userInfo.get("name");
            String userId = (String) userInfo.get("id");
            
            // Create or update user
            User user = userService.findByRedditUsername(username);
            if (user == null) {
                user = new User();
                user.setRedditUsername(username);
                user.setRedditUserId(userId);
                logger.info("Creating new user: {}", username);
            } else {
                logger.info("Updating existing user: {}", username);
            }
            
            // Update tokens
            user.setAccessToken(tokenResponse.getAccessToken());
            user.setRefreshToken(tokenResponse.getRefreshToken());
            user.setTokenExpiresAt(redditApiUtil.calculateTokenExpiry(tokenResponse.getExpiresIn()));
            user.setIsActive(true);
            
            return userService.save(user);
            
        } catch (Exception e) {
            logger.error("Error completing OAuth flow: {}", e.getMessage());
            return null;
        }
    }
    
    /**
     * Check and refresh token if needed
     */
    public boolean ensureValidToken(User user) {
        if (redditApiUtil.isTokenExpired(user.getTokenExpiresAt())) {
            logger.info("Token expired for user: {}. Refreshing...", user.getRedditUsername());
            
            RedditTokenResponse tokenResponse = refreshAccessToken(user.getRefreshToken());
            if (tokenResponse != null) {
                user.setAccessToken(tokenResponse.getAccessToken());
                user.setTokenExpiresAt(redditApiUtil.calculateTokenExpiry(tokenResponse.getExpiresIn()));
                userService.save(user);
                logger.info("Token refreshed successfully for user: {}", user.getRedditUsername());
                return true;
            } else {
                logger.error("Failed to refresh token for user: {}", user.getRedditUsername());
                return false;
            }
        }
        return true;
    }
}
"""
        },

        {
            "path": "src\\main\\java\\com\\anuj\\redditmessagemanager\\service\\UserService.java",
            "content": """package com.anuj.redditmessagemanager.service;

import com.anuj.redditmessagemanager.dto.UserDto;
import com.anuj.redditmessagemanager.entity.User;
import com.anuj.redditmessagemanager.repository.UserRepository;
import com.anuj.redditmessagemanager.repository.RedditMessageRepository;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.time.LocalDateTime;
import java.util.List;
import java.util.Optional;

@Service
@Transactional
public class UserService {
    
    private static final Logger logger = LoggerFactory.getLogger(UserService.class);
    
    @Autowired
    private UserRepository userRepository;
    
    @Autowired
    private RedditMessageRepository messageRepository;
    
    /**
     * Save or update user
     */
    public User save(User user) {
        try {
            User savedUser = userRepository.save(user);
            logger.info("User saved successfully: {}", savedUser.getRedditUsername());
            return savedUser;
        } catch (Exception e) {
            logger.error("Error saving user: {}", e.getMessage());
            throw new RuntimeException("Failed to save user", e);
        }
    }
    
    /**
     * Find user by ID
     */
    public User findById(Long id) {
        Optional<User> user = userRepository.findById(id);
        return user.orElse(null);
    }
    
    /**
     * Find user by Reddit username
     */
    public User findByRedditUsername(String username) {
        Optional<User> user = userRepository.findByRedditUsername(username);
        return user.orElse(null);
    }
    
    /**
     * Find user by Reddit user ID
     */
    public User findByRedditUserId(String userId) {
        Optional<User> user = userRepository.findByRedditUserId(userId);
        return user.orElse(null);
    }
    
    /**
     * Find user by access token
     */
    public User findByAccessToken(String accessToken) {
        Optional<User> user = userRepository.findByAccessToken(accessToken);
        return user.orElse(null);
    }
    
    /**
     * Check if user exists by username
     */
    public boolean existsByUsername(String username) {
        return userRepository.existsByRedditUsername(username);
    }
    
    /**
     * Get all active users
     */
    public List<User> findAllActiveUsers() {
        return userRepository.findByIsActiveTrue();
    }
    
    /**
     * Get users with expired tokens
     */
    public List<User> findUsersWithExpiredTokens() {
        return userRepository.findUsersWithExpiredTokens(LocalDateTime.now());
    }
    
    /**
     * Deactivate user
     */
    public void deactivateUser(Long userId) {
        try {
            userRepository.deactivateUser(userId);
            logger.info("User deactivated: {}", userId);
        } catch (Exception e) {
            logger.error("Error deactivating user {}: {}", userId, e.getMessage());
            throw new RuntimeException("Failed to deactivate user", e);
        }
    }
    
    /**
     * Update user token
     */
    public void updateUserToken(Long userId, String accessToken, LocalDateTime expiresAt) {
        try {
            userRepository.updateUserToken(userId, accessToken, expiresAt);
            logger.info("Token updated for user: {}", userId);
        } catch (Exception e) {
            logger.error("Error updating token for user {}: {}", userId, e.getMessage());
            throw new RuntimeException("Failed to update user token", e);
        }
    }
    
    /**
     * Convert user to DTO
     */
    public UserDto convertToDto(User user) {
        if (user == null) {
            return null;
        }
        
        UserDto dto = new UserDto();
        dto.setId(user.getId());
        dto.setRedditUsername(user.getRedditUsername());
        dto.setRedditUserId(user.getRedditUserId());
        dto.setIsActive(user.getIsActive());
        dto.setCreatedAt(user.getCreatedAt());
        
        // Get message counts
        dto.setMessageCount(messageRepository.countByUserAndMessageType(user, null));
        dto.setUnreadCount(messageRepository.countByUserAndIsReadFalse(user));
        
        return dto;
    }
    
    /**
     * Get user statistics
     */
    public UserDto getUserStatistics(String username) {
        User user = findByRedditUsername(username);
        if (user == null) {
            return null;
        }
        
        return convertToDto(user);
    }
    
    /**
     * Delete user and all associated data
     */
    @Transactional
    public void deleteUser(Long userId) {
        try {
            User user = findById(userId);
            if (user != null) {
                // Messages will be deleted automatically due to cascade
                userRepository.delete(user);
                logger.info("User deleted successfully: {}", user.getRedditUsername());
            }
        } catch (Exception e) {
            logger.error("Error deleting user {}: {}", userId, e.getMessage());
            throw new RuntimeException("Failed to delete user", e);
        }
    }
    
    /**
     * Clean up inactive users (older than specified days)
     */
    public int cleanupInactiveUsers(int daysInactive) {
        try {
            LocalDateTime cutoffDate = LocalDateTime.now().minusDays(daysInactive);
            List<User> inactiveUsers = userRepository.findByCreatedAtBetween(
                LocalDateTime.of(2000, 1, 1, 0, 0), cutoffDate);
            
            int deletedCount = 0;
            for (User user : inactiveUsers) {
                if (!user.getIsActive()) {
                    userRepository.delete(user);
                    deletedCount++;
                }
            }
            
            logger.info("Cleaned up {} inactive users", deletedCount);
            return deletedCount;
            
        } catch (Exception e) {
            logger.error("Error cleaning up inactive users: {}", e.getMessage());
            throw new RuntimeException("Failed to cleanup inactive users", e);
        }
    }
}
"""
        },

        {
            "path": "src\\main\\java\\com\\anuj\\redditmessagemanager\\service\\RedditMessageService.java",
            "content": """package com.anuj.redditmessagemanager.service;

import com.anuj.redditmessagemanager.dto.RedditApiMessageResponse;
import com.anuj.redditmessagemanager.dto.RedditMessageDto;
import com.anuj.redditmessagemanager.entity.RedditMessage;
import com.anuj.redditmessagemanager.entity.RedditMessage.MessageType;
import com.anuj.redditmessagemanager.entity.User;
import com.anuj.redditmessagemanager.repository.RedditMessageRepository;
import com.anuj.redditmessagemanager.util.RedditApiUtil;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageRequest;
import org.springframework.data.domain.Pageable;
import org.springframework.http.HttpEntity;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpMethod;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import org.springframework.web.client.RestTemplate;

import java.time.LocalDateTime;
import java.util.List;

@Service
@Transactional
public class RedditMessageService {
    
    private static final Logger logger = LoggerFactory.getLogger(RedditMessageService.class);
    
    @Autowired
    private RedditMessageRepository messageRepository;
    
    @Autowired
    private RestTemplate restTemplate;
    
    @Autowired
    private RedditApiUtil redditApiUtil;
    
    @Autowired
    private RedditOAuthService oauthService;
    
    /**
     * Fetch messages from Reddit API and store in database
     */
    public List<RedditMessageDto> fetchAndStoreMessages(User user, MessageType messageType) {
        try {
            // Ensure valid token
            if (!oauthService.ensureValidToken(user)) {
                throw new RuntimeException("Failed to refresh user token");
            }
            
            String endpoint = getEndpointForMessageType(messageType);
            RedditApiMessageResponse response = fetchMessagesFromReddit(user.getAccessToken(), endpoint);
            
            if (response != null) {
                List<RedditMessage> messages = redditApiUtil.convertApiResponseToMessages(response, user, messageType);
                
                // Save new messages (avoid duplicates)
                int savedCount = 0;
                for (RedditMessage message : messages) {
                    if (!messageRepository.existsByRedditMessageId(message.getRedditMessageId())) {
                        messageRepository.save(message);
                        savedCount++;
                    }
                }
                
                logger.info("Fetched and saved {} new {} messages for user: {}", 
                    savedCount, messageType, user.getRedditUsername());
                
                return redditApiUtil.convertToDtoList(messages);
            }
            
        } catch (Exception e) {
            logger.error("Error fetching messages for user {}: {}", user.getRedditUsername(), e.getMessage());
            throw new RuntimeException("Failed to fetch messages", e);
        }
        
        return List.of();
    }
    
    /**
     * Get stored messages by type
     */
    public List<RedditMessageDto> getMessagesByType(User user, MessageType messageType) {
        List<RedditMessage> messages = messageRepository.findByUserAndMessageTypeOrderByStoredAtDesc(user, messageType);
        return redditApiUtil.convertToDtoList(messages);
    }
    
    /**
     * Get all messages for user with pagination
     */
    public Page<RedditMessageDto> getAllMessages(User user, int page, int size) {
        Pageable pageable = PageRequest.of(page, size);
        Page<RedditMessage> messagePage = messageRepository.findByUserOrderByStoredAtDesc(user, pageable);
        
        return messagePage.map(redditApiUtil::convertToDto);
    }
    
    /**
     * Get unread messages
     */
    public List<RedditMessageDto> getUnreadMessages(User user) {
        List<RedditMessage> messages = messageRepository.findByUserAndIsReadFalseOrderByStoredAtDesc(user);
        return redditApiUtil.convertToDtoList(messages);
    }
    
    /**
     * Search messages by content
     */
    public List<RedditMessageDto> searchMessages(User user, String searchTerm) {
        List<RedditMessage> messages = messageRepository.searchMessagesByContent(user, searchTerm);
        return redditApiUtil.convertToDtoList(messages);
    }
    
    /**
     * Search messages by author
     */
    public List<RedditMessageDto> searchMessagesByAuthor(User user, String author) {
        List<RedditMessage> messages = messageRepository.findByUserAndAuthorContainingIgnoreCaseOrderByStoredAtDesc(user, author);
        return redditApiUtil.convertToDtoList(messages);
    }
    
    /**
     * Search messages by subreddit
     */
    public List<RedditMessageDto> searchMessagesBySubreddit(User user, String subreddit) {
        List<RedditMessage> messages = messageRepository.findByUserAndSubredditContainingIgnoreCaseOrderByStoredAtDesc(user, subreddit);
        return redditApiUtil.convertToDtoList(messages);
    }
    
    /**
     * Mark message as read
     */
    public void markMessageAsRead(User user, Long messageId) {
        try {
            messageRepository.markMessageAsRead(messageId, user);
            logger.info("Message {} marked as read for user: {}", messageId, user.getRedditUsername());
        } catch (Exception e) {
            logger.error("Error marking message as read: {}", e.getMessage());
            throw new RuntimeException("Failed to mark message as read", e);
        }
    }
    
    /**
     * Mark all messages as read
     */
    public void markAllMessagesAsRead(User user) {
        try {
            messageRepository.markAllMessagesAsRead(user);
            logger.info("All messages marked as read for user: {}", user.getRedditUsername());
        } catch (Exception e) {
            logger.error("Error marking all messages as read: {}", e.getMessage());
            throw new RuntimeException("Failed to mark all messages as read", e);
        }
    }
    
    /**
     * Get message statistics
     */
    public RedditMessageDto getMessageStatistics(User user) {
        long totalMessages = messageRepository.countByUserAndMessageType(user, null);
        long unreadCount = messageRepository.countByUserAndIsReadFalse(user);
        long inboxCount = messageRepository.countByUserAndMessageType(user, MessageType.INBOX);
        long sentCount = messageRepository.countByUserAndMessageType(user, MessageType.SENT);
        
        RedditMessageDto stats = new RedditMessageDto();
        stats.setSubject("Statistics");
        stats.setBody(String.format("Total: %d, Unread: %d, Inbox: %d, Sent: %d", 
            totalMessages, unreadCount, inboxCount, sentCount));
        
        return stats;
    }
    
    /**
     * Delete old messages
     */
    public int deleteOldMessages(User user, int daysOld) {
        try {
            LocalDateTime cutoffDate = LocalDateTime.now().minusDays(daysOld);
            long countBefore = messageRepository.countByUserAndMessageType(user, null);
            
            messageRepository.deleteByUserAndStoredAtBefore(user, cutoffDate);
            
            long countAfter = messageRepository.countByUserAndMessageType(user, null);
            int deletedCount = (int) (countBefore - countAfter);
            
            logger.info("Deleted {} old messages for user: {}", deletedCount, user.getRedditUsername());
            return deletedCount;
            
        } catch (Exception e) {
            logger.error("Error deleting old messages: {}", e.getMessage());
            throw new RuntimeException("Failed to delete old messages", e);
        }
    }
    
    /**
     * Get messages by date range
     */
    public List<RedditMessageDto> getMessagesByDateRange(User user, LocalDateTime startDate, LocalDateTime endDate) {
        List<RedditMessage> messages = messageRepository.findByUserAndStoredAtBetweenOrderByStoredAtDesc(user, startDate, endDate);
        return redditApiUtil.convertToDtoList(messages);
    }
    
    /**
     * Fetch messages from Reddit API
     */
    private RedditApiMessageResponse fetchMessagesFromReddit(String accessToken, String endpoint) {
        try {
            HttpHeaders headers = new HttpHeaders();
            headers.set("Authorization", "Bearer " + accessToken);
            headers.set("User-Agent", "RedditMessageManager/1.0");
            
            HttpEntity<String> entity = new HttpEntity<>(headers);
            
            ResponseEntity<RedditApiMessageResponse> response = restTemplate.exchange(
                "https://oauth.reddit.com" + endpoint,
                HttpMethod.GET,
                entity,
                RedditApiMessageResponse.class
            );
            
            if (response.getStatusCode().is2xxSuccessful()) {
                return response.getBody();
            } else {
                logger.error("Failed to fetch messages. Status: {}", response.getStatusCode());
                return null;
            }
            
        } catch (Exception e) {
            logger.error("Error fetching messages from Reddit: {}", e.getMessage());
            return null;
        }
    }
    
    /**
     * Get API endpoint for message type
     */
    private String getEndpointForMessageType(MessageType messageType) {
        return switch (messageType) {
            case INBOX -> "/message/inbox";
            case SENT -> "/message/sent";
            case UNREAD -> "/message/unread";
            default -> "/message/inbox";
        };
    }
}
"""
        },

        {
            "path": "src\\main\\java\\com\\anuj\\redditmessagemanager\\service\\SearchService.java",
            "content": """package com.anuj.redditmessagemanager.service;

import com.anuj.redditmessagemanager.dto.RedditMessageDto;
import com.anuj.redditmessagemanager.dto.SearchResultDto;
import com.anuj.redditmessagemanager.entity.SearchHistory;
import com.anuj.redditmessagemanager.entity.SearchHistory.SearchType;
import com.anuj.redditmessagemanager.entity.User;
import com.anuj.redditmessagemanager.repository.SearchHistoryRepository;
import com.anuj.redditmessagemanager.util.ValidationUtil;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpEntity;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpMethod;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import org.springframework.web.client.RestTemplate;

import java.time.LocalDateTime;
import java.util.List;
import java.util.Map;

@Service
@Transactional
public class SearchService {
    
    private static final Logger logger = LoggerFactory.getLogger(SearchService.class);
    
    @Autowired
    private SearchHistoryRepository searchHistoryRepository;
    
    @Autowired
    private RedditMessageService messageService;
    
    @Autowired
    private RedditOAuthService oauthService;
    
    @Autowired
    private RestTemplate restTemplate;
    
    @Autowired
    private ValidationUtil validationUtil;
    
    /**
     * Search messages in local database
     */
    public SearchResultDto searchMessages(User user, String query) {
        if (!validationUtil.isValidSearchQuery(query)) {
            throw new IllegalArgumentException("Invalid search query");
        }
        
        String sanitizedQuery = validationUtil.sanitizeSearchQuery(query);
        
        try {
            List<RedditMessageDto> messages = messageService.searchMessages(user, sanitizedQuery);
            
            // Save search history
            saveSearchHistory(user, sanitizedQuery, SearchType.MESSAGES, messages.size());
            
            SearchResultDto result = new SearchResultDto();
            result.setSearchQuery(sanitizedQuery);
            result.setSearchType(SearchType.MESSAGES);
            result.setMessages(messages);
            result.setTotalResults(messages.size());
            
            logger.info("Message search completed for user {}: {} results", 
                user.getRedditUsername(), messages.size());
            
            return result;
            
        } catch (Exception e) {
            logger.error("Error searching messages for user {}: {}", user.getRedditUsername(), e.getMessage());
            throw new RuntimeException("Failed to search messages", e);
        }
    }
    
    /**
     * Search Reddit posts via API
     */
    @SuppressWarnings("unchecked")
    public SearchResultDto searchRedditPosts(User user, String query) {
        if (!validationUtil.isValidSearchQuery(query)) {
            throw new IllegalArgumentException("Invalid search query");
        }
        
        String sanitizedQuery = validationUtil.sanitizeSearchQuery(query);
        
        try {
            // Ensure valid token
            if (!oauthService.ensureValidToken(user)) {
                throw new RuntimeException("Failed to refresh user token");
            }
            
            HttpHeaders headers = new HttpHeaders();
            headers.set("Authorization", "Bearer " + user.getAccessToken());
            headers.set("User-Agent", "RedditMessageManager/1.0");
            
            HttpEntity<String> entity = new HttpEntity<>(headers);
            
            String url = String.format("https://oauth.reddit.com/search.json?q=%s&limit=25", 
                sanitizedQuery.replace(" ", "%20"));
            
            ResponseEntity<Map> response = restTemplate.exchange(
                url, HttpMethod.GET, entity, Map.class
            );
            
            SearchResultDto result = new SearchResultDto();
            result.setSearchQuery(sanitizedQuery);
            result.setSearchType(SearchType.POSTS);
            
            if (response.getStatusCode().is2xxSuccessful() && response.getBody() != null) {
                Map<String, Object> data = (Map<String, Object>) response.getBody().get("data");
                List<Object> children = (List<Object>) data.get("children");
                
                result.setPosts(children);
                result.setTotalResults(children != null ? children.size() : 0);
                
                // Save search history
                saveSearchHistory(user, sanitizedQuery, SearchType.POSTS, result.getTotalResults());
                
                logger.info("Reddit post search completed for user {}: {} results", 
                    user.getRedditUsername(), result.getTotalResults());
            } else {
                result.setTotalResults(0);
                logger.warn("No results from Reddit post search for query: {}", sanitizedQuery);
            }
            
            return result;
            
        } catch (Exception e) {
            logger.error("Error searching Reddit posts for user {}: {}", user.getRedditUsername(), e.getMessage());
            throw new RuntimeException("Failed to search Reddit posts", e);
        }
    }
    
    /**
     * Search messages by author
     */
    public SearchResultDto searchByAuthor(User user, String author) {
        if (!validationUtil.isValidRedditUsername(author)) {
            throw new IllegalArgumentException("Invalid username format");
        }
        
        try {
            List<RedditMessageDto> messages = messageService.searchMessagesByAuthor(user, author);
            
            // Save search history
            saveSearchHistory(user, "author:" + author, SearchType.MESSAGES, messages.size());
            
            SearchResultDto result = new SearchResultDto();
            result.setSearchQuery("author:" + author);
            result.setSearchType(SearchType.MESSAGES);
            result.setMessages(messages);
            result.setTotalResults(messages.size());
            
            logger.info("Author search completed for user {}: {} results", 
                user.getRedditUsername(), messages.size());
            
            return result;
            
        } catch (Exception e) {
            logger.error("Error searching by author for user {}: {}", user.getRedditUsername(), e.getMessage());
            throw new RuntimeException("Failed to search by author", e);
        }
    }
    
    /**
     * Search messages by subreddit
     */
    public SearchResultDto searchBySubreddit(User user, String subreddit) {
        if (!validationUtil.isValidSubredditName(subreddit)) {
            throw new IllegalArgumentException("Invalid subreddit name format");
        }
        
        try {
            List<RedditMessageDto> messages = messageService.searchMessagesBySubreddit(user, subreddit);
            
            // Save search history
            saveSearchHistory(user, "r/" + subreddit, SearchType.MESSAGES, messages.size());
            
            SearchResultDto result = new SearchResultDto();
            result.setSearchQuery("r/" + subreddit);
            result.setSearchType(SearchType.MESSAGES);
            result.setMessages(messages);
            result.setTotalResults(messages.size());
            
            logger.info("Subreddit search completed for user {}: {} results", 
                user.getRedditUsername(), messages.size());
            
            return result;
            
        } catch (Exception e) {
            logger.error("Error searching by subreddit for user {}: {}", user.getRedditUsername(), e.getMessage());
            throw new RuntimeException("Failed to search by subreddit", e);
        }
    }
    
    /**
     * Get search history for user
     */
    public List<SearchHistory> getSearchHistory(User user) {
        return searchHistoryRepository.findTop10ByUserOrderBySearchedAtDesc(user);
    }
    
    /**
     * Get popular search terms for user
     */
    public List<Object[]> getPopularSearchTerms(User user) {
        return searchHistoryRepository.findMostPopularSearchTerms(user);
    }
    
    /**
     * Clear search history for user
     */
    public void clearSearchHistory(User user) {
        try {
            List<SearchHistory> userSearches = searchHistoryRepository.findByUserOrderBySearchedAtDesc(user);
            searchHistoryRepository.deleteAll(userSearches);
            logger.info("Search history cleared for user: {}", user.getRedditUsername());
        } catch (Exception e) {
            logger.error("Error clearing search history for user {}: {}", user.getRedditUsername(), e.getMessage());
            throw new RuntimeException("Failed to clear search history", e);
        }
    }
    
    /**
     * Delete old search history
     */
    public int deleteOldSearchHistory(User user, int daysOld) {
        try {
            LocalDateTime cutoffDate = LocalDateTime.now().minusDays(daysOld);
            long countBefore = searchHistoryRepository.countByUser(user);
            
            searchHistoryRepository.deleteByUserAndSearchedAtBefore(user, cutoffDate);
            
            long countAfter = searchHistoryRepository.countByUser(user);
            int deletedCount = (int) (countBefore - countAfter);
            
            logger.info("Deleted {} old search history entries for user: {}", 
                deletedCount, user.getRedditUsername());
            
            return deletedCount;
            
        } catch (Exception e) {
            logger.error("Error deleting old search history: {}", e.getMessage());
            throw new RuntimeException("Failed to delete old search history", e);
        }
    }
    
    /**
     * Save search history entry
     */
    private void saveSearchHistory(User user, String query, SearchType searchType, Integer resultsCount) {
        try {
            SearchHistory searchHistory = new SearchHistory(query, searchType, resultsCount, user);
            searchHistoryRepository.save(searchHistory);
        } catch (Exception e) {
            logger.warn("Failed to save search history: {}", e.getMessage());
            // Don't throw exception as this is not critical
        }
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

    # Create service files
    create_files(service_files, "Service")

    print("\n" + "="*70)
    print("Service classes created successfully!")
    print("="*70)

    print("\nCreated Service Classes:")
    print("✓ RedditOAuthService.java - OAuth2 authentication and token management")
    print("✓ UserService.java - User management and operations")
    print("✓ RedditMessageService.java - Message fetching, storing, and management")
    print("✓ SearchService.java - Search functionality and history tracking")

    print("\nService Features:")
    print("• Complete OAuth2 flow with token refresh")
    print("• Reddit API integration for message fetching")
    print("• Local message storage and management")
    print("• Advanced search capabilities (content, author, subreddit)")
    print("• Search history tracking and analytics")
    print("• User management with statistics")
    print("• Error handling and logging")
    print("• Transaction management")
    print("• Token expiry handling")
    print("• Data cleanup utilities")

    print("\nKey Methods Available:")
    print("RedditOAuthService:")
    print("  - completeOAuthFlow() - Handle Reddit login")
    print("  - ensureValidToken() - Auto-refresh expired tokens")
    print("  - exchangeCodeForToken() - OAuth code exchange")

    print("\nRedditMessageService:")
    print("  - fetchAndStoreMessages() - Get messages from Reddit API")
    print("  - searchMessages() - Search local message database")
    print("  - markMessageAsRead() - Mark messages as read")

    print("\nSearchService:")
    print("  - searchMessages() - Search messages with history tracking")
    print("  - searchRedditPosts() - Search Reddit posts via API")
    print("  - searchByAuthor() - Find messages by author")
    print("  - searchBySubreddit() - Find messages by subreddit")

    print("\nUserService:")
    print("  - save() - Create/update users")
    print("  - findByRedditUsername() - Find user by Reddit username")
    print("  - getUserStatistics() - Get user message statistics")

    print("\nNext steps:")
    print("1. Create controller classes")
    print("2. Test the service methods")
    print("3. Run the application")
    print("4. Test OAuth2 flow")
    print("5. Test message fetching and search")

if __name__ == "__main__":
    create_service_classes()
