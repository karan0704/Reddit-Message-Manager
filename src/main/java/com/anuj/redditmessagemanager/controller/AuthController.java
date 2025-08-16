package com.anuj.redditmessagemanager.controller;

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
