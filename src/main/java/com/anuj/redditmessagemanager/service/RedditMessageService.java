package com.anuj.redditmessagemanager.service;

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
