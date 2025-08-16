package com.anuj.redditmessagemanager.dto;

import com.fasterxml.jackson.annotation.JsonProperty;
import lombok.Data;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;

import java.time.LocalDateTime;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class AuthDto {
    
    private String username;
    
    private String password;
    
    @JsonProperty("display_name")
    private String displayName;
    
    private String email;
    
    @JsonProperty("remember_me")
    private Boolean rememberMe;
    
    @JsonProperty("is_authenticated")
    private Boolean isAuthenticated;
    
    @JsonProperty("session_token")
    private String sessionToken;
    
    @JsonProperty("login_time")
    private LocalDateTime loginTime;
    
    @JsonProperty("last_activity")
    private LocalDateTime lastActivity;
    
    @JsonProperty("user_agent")
    private String userAgent;
    
    @JsonProperty("ip_address")
    private String ipAddress;
    
    @JsonProperty("is_remembered_user")
    private Boolean isRememberedUser = false;
    
    @JsonProperty("previous_login")
    private LocalDateTime previousLogin;
    
    // Constructor for login requests
    public AuthDto(String username, String password, Boolean rememberMe) {
        this.username = username;
        this.password = password;
        this.rememberMe = rememberMe != null ? rememberMe : false;
    }
    
    // Constructor for authentication responses
    public AuthDto(String username, String displayName, Boolean isAuthenticated, String sessionToken) {
        this.username = username;
        this.displayName = displayName;
        this.isAuthenticated = isAuthenticated;
        this.sessionToken = sessionToken;
        this.loginTime = LocalDateTime.now();
    }
    
    // Constructor for remembered user
    public static AuthDto createRememberedUser(String username, String displayName, LocalDateTime previousLogin) {
        AuthDto auth = new AuthDto();
        auth.setUsername(username);
        auth.setDisplayName(displayName);
        auth.setIsRememberedUser(true);
        auth.setPreviousLogin(previousLogin);
        auth.setRememberMe(true);
        return auth;
    }
}
