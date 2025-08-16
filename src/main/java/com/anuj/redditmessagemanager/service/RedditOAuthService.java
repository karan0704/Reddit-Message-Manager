package com.anuj.redditmessagemanager.service;

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
