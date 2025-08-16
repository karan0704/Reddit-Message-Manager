package com.anuj.redditmessagemanager.service;

import com.anuj.redditmessagemanager.entity.User;
import com.anuj.redditmessagemanager.repository.UserRepository;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.time.LocalDateTime;
import java.util.UUID;

@Service
@Transactional
public class LocalAuthService {
    
    private static final Logger logger = LoggerFactory.getLogger(LocalAuthService.class);
    
    @Autowired
    private UserRepository userRepository;
    
    /**
     * Authenticate user with username and password (mock authentication)
     */
    public User authenticateUser(String username, String password) {
        try {
            // In a real app, you'd hash and verify password
            // For this local app, we'll do simple mock authentication
            User user = userRepository.findByUsername(username).orElse(null);
            
            if (user != null && user.getIsActive()) {
                // Mock password check (in real app, use BCrypt or similar)
                if (isPasswordValid(user, password)) {
                    updateUserOnlineStatus(user, true);
                    logger.info("User authenticated: {}", username);
                    return user;
                }
            }
            
            logger.warn("Authentication failed for username: {}", username);
            return null;
            
        } catch (Exception e) {
            logger.error("Error during authentication: {}", e.getMessage());
            return null;
        }
    }
    
    /**
     * Create new user (mock registration)
     */
    public User createUser(String username, String displayName, String email, String password) {
        try {
            if (userRepository.existsByUsername(username)) {
                throw new RuntimeException("Username already exists");
            }
            
            if (email != null && userRepository.existsByEmail(email)) {
                throw new RuntimeException("Email already exists");
            }
            
            User user = new User();
            user.setUsername(username);
            user.setDisplayName(displayName != null ? displayName : username);
            user.setEmail(email);
            user.setPasswordHash(hashPassword(password)); // Mock password hashing
            user.setIsActive(true);
            user.setIsOnline(false);
            user.setIsRemembered(false);
            
            User savedUser = userRepository.save(user);
            logger.info("New user created: {}", username);
            return savedUser;
            
        } catch (Exception e) {
            logger.error("Error creating user: {}", e.getMessage());
            throw new RuntimeException("Failed to create user", e);
        }
    }
    
    /**
     * Generate session token
     */
    public String generateSessionToken(String username) {
        return UUID.randomUUID().toString() + "_" + username + "_" + System.currentTimeMillis();
    }
    
    /**
     * Update user online status
     */
    public void updateUserOnlineStatus(User user, boolean isOnline) {
        try {
            userRepository.updateOnlineStatus(user.getUsername(), isOnline, LocalDateTime.now());
            
            if (!isOnline) {
                logger.info("User went offline: {}", user.getUsername());
            }
        } catch (Exception e) {
            logger.error("Error updating online status: {}", e.getMessage());
        }
    }
    
    /**
     * Mock password validation
     */
    private boolean isPasswordValid(User user, String password) {
        // In a real app, use BCrypt.checkpw(password, user.getPasswordHash())
        // For mock purposes, we'll accept any password for existing users
        return password != null && !password.trim().isEmpty();
    }
    
    /**
     * Mock password hashing
     */
    private String hashPassword(String password) {
        // In a real app, use BCrypt.hashpw(password, BCrypt.gensalt())
        // For mock purposes, we'll just store a simple hash
        return "mock_hash_" + password.hashCode();
    }
    
    /**
     * Validate session token
     */
    public boolean isValidSessionToken(String token, String username) {
        // Simple validation - in real app, store tokens in database or cache
        return token != null && token.contains(username);
    }
}
