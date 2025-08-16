package com.anuj.redditmessagemanager.util;

import org.springframework.stereotype.Component;
import org.springframework.util.StringUtils;

import java.util.regex.Pattern;

@Component
public class ValidationUtil {
    
    private static final Pattern USERNAME_PATTERN = Pattern.compile("^[a-zA-Z0-9_-]{3,20}$");
    private static final Pattern SUBREDDIT_PATTERN = Pattern.compile("^[a-zA-Z0-9_]{2,21}$");
    
    /**
     * Validate Reddit username format
     */
    public boolean isValidRedditUsername(String username) {
        return StringUtils.hasText(username) && USERNAME_PATTERN.matcher(username).matches();
    }
    
    /**
     * Validate subreddit name format
     */
    public boolean isValidSubredditName(String subreddit) {
        return StringUtils.hasText(subreddit) && SUBREDDIT_PATTERN.matcher(subreddit).matches();
    }
    
    /**
     * Validate search query
     */
    public boolean isValidSearchQuery(String query) {
        return StringUtils.hasText(query) && 
               query.length() >= 2 && 
               query.length() <= 500 &&
               !query.trim().isEmpty();
    }
    
    /**
     * Validate access token format
     */
    public boolean isValidAccessToken(String token) {
        return StringUtils.hasText(token) && 
               token.length() > 10 && 
               token.length() < 2000;
    }
    
    /**
     * Sanitize search query
     */
    /**
     * Sanitize search query
     */
    public String sanitizeSearchQuery(String query) {
        if (!StringUtils.hasText(query)) {
            return "";
        }

        return query.trim()
                .replaceAll("[<>\"'&]", "") // Remove potentially dangerous characters
                .substring(0, Math.min(query.length(), 500)); // Limit length
    }
    
    /**
     * Validate message ID format
     */
    public boolean isValidMessageId(String messageId) {
        return StringUtils.hasText(messageId) && 
               messageId.length() >= 5 && 
               messageId.length() <= 50 &&
               messageId.matches("^[a-zA-Z0-9_]+$");
    }
    
    /**
     * Check if string is not null or empty
     */
    public boolean isNotEmpty(String value) {
        return StringUtils.hasText(value);
    }
    
    /**
     * Validate page number for pagination
     */
    public boolean isValidPageNumber(Integer page) {
        return page != null && page > 0;
    }
    
    /**
     * Validate page size for pagination
     */
    public boolean isValidPageSize(Integer size) {
        return size != null && size > 0 && size <= 100;
    }
}
