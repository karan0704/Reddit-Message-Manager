import os

def create_config_dto_util_code():
    # Base path from your previous conversation
    base_path = "D:\\Karan Ticket Project\\Reddit Message Manager"

    # Config classes
    config_files = [
        {
            "path": "src\\main\\java\\com\\anuj\\redditmessagemanager\\config\\RedditConfig.java",
            "content": """package com.anuj.redditmessagemanager.config;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.web.client.RestTemplate;
import org.springframework.web.reactive.function.client.WebClient;

@Configuration
public class RedditConfig {
    
    @Value("${reddit.client.id}")
    private String clientId;
    
    @Value("${reddit.client.secret}")
    private String clientSecret;
    
    @Value("${reddit.redirect.uri}")
    private String redirectUri;
    
    @Bean
    public RestTemplate restTemplate() {
        return new RestTemplate();
    }
    
    @Bean
    public WebClient webClient() {
        return WebClient.builder()
                .baseUrl("https://oauth.reddit.com")
                .defaultHeader("User-Agent", "RedditMessageManager/1.0")
                .build();
    }
    
    public String getClientId() {
        return clientId;
    }
    
    public String getClientSecret() {
        return clientSecret;
    }
    
    public String getRedirectUri() {
        return redirectUri;
    }
    
    public String getAuthorizationUrl() {
        return "https://www.reddit.com/api/v1/authorize?" +
                "client_id=" + clientId +
                "&response_type=code" +
                "&state=%s" +
                "&redirect_uri=" + redirectUri +
                "&duration=permanent" +
                "&scope=read+privatemessages+identity+submit";
    }
}
"""
        },

        {
            "path": "src\\main\\java\\com\\anuj\\redditmessagemanager\\config\\WebConfig.java",
            "content": """package com.anuj.redditmessagemanager.config;

import org.springframework.context.annotation.Configuration;
import org.springframework.web.servlet.config.annotation.CorsRegistry;
import org.springframework.web.servlet.config.annotation.ResourceHandlerRegistry;
import org.springframework.web.servlet.config.annotation.ViewControllerRegistry;
import org.springframework.web.servlet.config.annotation.WebMvcConfigurer;

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
                .addResourceLocations("classpath:/static/");
    }
    
    @Override
    public void addViewControllers(ViewControllerRegistry registry) {
        registry.addViewController("/").setViewName("index");
        registry.addViewController("/dashboard").setViewName("dashboard");
        registry.addViewController("/error").setViewName("error");
    }
}
"""
        },

        {
            "path": "src\\main\\java\\com\\anuj\\redditmessagemanager\\config\\SecurityConfig.java",
            "content": """package com.anuj.redditmessagemanager.config;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.config.annotation.web.configuration.EnableWebSecurity;
import org.springframework.security.web.SecurityFilterChain;
import org.springframework.security.web.util.matcher.AntPathRequestMatcher;

@Configuration
@EnableWebSecurity
public class SecurityConfig {
    
    @Bean
    public SecurityFilterChain filterChain(HttpSecurity http) throws Exception {
        http
            .csrf(csrf -> csrf.disable())
            .authorizeHttpRequests(authz -> authz
                .requestMatchers(
                    new AntPathRequestMatcher("/"),
                    new AntPathRequestMatcher("/login"),
                    new AntPathRequestMatcher("/auth/callback"),
                    new AntPathRequestMatcher("/static/**"),
                    new AntPathRequestMatcher("/css/**"),
                    new AntPathRequestMatcher("/js/**"),
                    new AntPathRequestMatcher("/images/**"),
                    new AntPathRequestMatcher("/error")
                ).permitAll()
                .anyRequest().authenticated()
            )
            .sessionManagement(session -> session
                .maximumSessions(1)
                .maxSessionsPreventsLogin(false)
            );
        
        return http.build();
    }
}
"""
        }
    ]

    # DTO classes
    dto_files = [
        {
            "path": "src\\main\\java\\com\\anuj\\redditmessagemanager\\dto\\RedditTokenResponse.java",
            "content": """package com.anuj.redditmessagemanager.dto;

import com.fasterxml.jackson.annotation.JsonProperty;
import lombok.Data;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class RedditTokenResponse {
    
    @JsonProperty("access_token")
    private String accessToken;
    
    @JsonProperty("token_type")
    private String tokenType;
    
    @JsonProperty("expires_in")
    private Integer expiresIn;
    
    @JsonProperty("refresh_token")
    private String refreshToken;
    
    @JsonProperty("scope")
    private String scope;
}
"""
        },

        {
            "path": "src\\main\\java\\com\\anuj\\redditmessagemanager\\dto\\RedditMessageDto.java",
            "content": """package com.anuj.redditmessagemanager.dto;

import com.anuj.redditmessagemanager.entity.RedditMessage.MessageType;
import com.fasterxml.jackson.annotation.JsonProperty;
import lombok.Data;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;

import java.time.LocalDateTime;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class RedditMessageDto {
    
    private Long id;
    
    @JsonProperty("reddit_message_id")
    private String redditMessageId;
    
    @JsonProperty("message_type")
    private MessageType messageType;
    
    private String subject;
    private String body;
    private String author;
    private String recipient;
    private String subreddit;
    
    @JsonProperty("is_read")
    private Boolean isRead;
    
    @JsonProperty("reddit_created_at")
    private LocalDateTime redditCreatedAt;
    
    private String context;
    
    @JsonProperty("parent_id")
    private String parentId;
    
    @JsonProperty("stored_at")
    private LocalDateTime storedAt;
    
    // Constructor for API responses
    public RedditMessageDto(String subject, String body, String author, MessageType messageType) {
        this.subject = subject;
        this.body = body;
        this.author = author;
        this.messageType = messageType;
        this.isRead = false;
    }
}
"""
        },

        {
            "path": "src\\main\\java\\com\\anuj\\redditmessagemanager\\dto\\UserDto.java",
            "content": """package com.anuj.redditmessagemanager.dto;

import com.fasterxml.jackson.annotation.JsonProperty;
import lombok.Data;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;

import java.time.LocalDateTime;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class UserDto {
    
    private Long id;
    
    @JsonProperty("reddit_username")
    private String redditUsername;
    
    @JsonProperty("reddit_user_id")
    private String redditUserId;
    
    @JsonProperty("is_active")
    private Boolean isActive;
    
    @JsonProperty("created_at")
    private LocalDateTime createdAt;
    
    @JsonProperty("message_count")
    private Long messageCount;
    
    @JsonProperty("unread_count")
    private Long unreadCount;
    
    // Constructor without sensitive data
    public UserDto(String redditUsername, String redditUserId, Boolean isActive, LocalDateTime createdAt) {
        this.redditUsername = redditUsername;
        this.redditUserId = redditUserId;
        this.isActive = isActive;
        this.createdAt = createdAt;
    }
}
"""
        },

        {
            "path": "src\\main\\java\\com\\anuj\\redditmessagemanager\\dto\\RedditApiMessageResponse.java",
            "content": """package com.anuj.redditmessagemanager.dto;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import com.fasterxml.jackson.annotation.JsonProperty;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.util.List;

@Data
@NoArgsConstructor
@JsonIgnoreProperties(ignoreUnknown = true)
public class RedditApiMessageResponse {
    
    @JsonProperty("kind")
    private String kind;
    
    @JsonProperty("data")
    private MessageData data;
    
    @Data
    @NoArgsConstructor
    @JsonIgnoreProperties(ignoreUnknown = true)
    public static class MessageData {
        
        @JsonProperty("children")
        private List<MessageChild> children;
        
        @JsonProperty("after")
        private String after;
        
        @JsonProperty("before")
        private String before;
    }
    
    @Data
    @NoArgsConstructor
    @JsonIgnoreProperties(ignoreUnknown = true)
    public static class MessageChild {
        
        @JsonProperty("kind")
        private String kind;
        
        @JsonProperty("data")
        private MessageDetails data;
    }
    
    @Data
    @NoArgsConstructor
    @JsonIgnoreProperties(ignoreUnknown = true)
    public static class MessageDetails {
        
        @JsonProperty("id")
        private String id;
        
        @JsonProperty("subject")
        private String subject;
        
        @JsonProperty("body")
        private String body;
        
        @JsonProperty("body_html")
        private String bodyHtml;
        
        @JsonProperty("author")
        private String author;
        
        @JsonProperty("dest")
        private String dest;
        
        @JsonProperty("subreddit")
        private String subreddit;
        
        @JsonProperty("created_utc")
        private Double createdUtc;
        
        @JsonProperty("new")
        private Boolean isNew;
        
        @JsonProperty("context")
        private String context;
        
        @JsonProperty("parent_id")
        private String parentId;
        
        @JsonProperty("first_message")
        private String firstMessage;
        
        @JsonProperty("name")
        private String name;
    }
}
"""
        },

        {
            "path": "src\\main\\java\\com\\anuj\\redditmessagemanager\\dto\\SearchResultDto.java",
            "content": """package com.anuj.redditmessagemanager.dto;

import com.anuj.redditmessagemanager.entity.SearchHistory.SearchType;
import lombok.Data;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;

import java.util.List;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class SearchResultDto {
    
    private String searchQuery;
    private SearchType searchType;
    private Integer totalResults;
    private List<RedditMessageDto> messages;
    private List<Object> posts; // For Reddit post searches
    private String nextPage;
    private String previousPage;
    
    public SearchResultDto(String searchQuery, SearchType searchType, List<RedditMessageDto> messages) {
        this.searchQuery = searchQuery;
        this.searchType = searchType;
        this.messages = messages;
        this.totalResults = messages != null ? messages.size() : 0;
    }
}
"""
        }
    ]

    # Util classes
    util_files = [
        {
            "path": "src\\main\\java\\com\\anuj\\redditmessagemanager\\util\\RedditApiUtil.java",
            "content": """package com.anuj.redditmessagemanager.util;

import com.anuj.redditmessagemanager.dto.RedditApiMessageResponse;
import com.anuj.redditmessagemanager.dto.RedditMessageDto;
import com.anuj.redditmessagemanager.entity.RedditMessage;
import com.anuj.redditmessagemanager.entity.RedditMessage.MessageType;
import com.anuj.redditmessagemanager.entity.User;
import org.springframework.stereotype.Component;

import java.time.LocalDateTime;
import java.time.ZoneOffset;
import java.util.ArrayList;
import java.util.Base64;
import java.util.List;
import java.util.UUID;

@Component
public class RedditApiUtil {
    
    /**
     * Create Basic Auth header for Reddit API
     */
    public String createBasicAuthHeader(String clientId, String clientSecret) {
        String credentials = clientId + ":" + clientSecret;
        return "Basic " + Base64.getEncoder().encodeToString(credentials.getBytes());
    }
    
    /**
     * Generate random state for OAuth
     */
    public String generateState() {
        return UUID.randomUUID().toString();
    }
    
    /**
     * Convert Reddit API response to message entities
     */
    public List<RedditMessage> convertApiResponseToMessages(RedditApiMessageResponse response, User user, MessageType messageType) {
        List<RedditMessage> messages = new ArrayList<>();
        
        if (response.getData() != null && response.getData().getChildren() != null) {
            for (RedditApiMessageResponse.MessageChild child : response.getData().getChildren()) {
                RedditApiMessageResponse.MessageDetails details = child.getData();
                
                RedditMessage message = new RedditMessage();
                message.setRedditMessageId(details.getId());
                message.setMessageType(messageType);
                message.setSubject(details.getSubject());
                message.setBody(details.getBody() != null ? details.getBody() : details.getBodyHtml());
                message.setAuthor(details.getAuthor());
                message.setRecipient(details.getDest());
                message.setSubreddit(details.getSubreddit());
                message.setIsRead(details.getIsNew() == null || !details.getIsNew());
                message.setContext(details.getContext());
                message.setParentId(details.getParentId());
                message.setUser(user);
                
                // Convert Reddit timestamp
                if (details.getCreatedUtc() != null) {
                    message.setRedditCreatedAt(
                        LocalDateTime.ofEpochSecond(details.getCreatedUtc().longValue(), 0, ZoneOffset.UTC)
                    );
                }
                
                messages.add(message);
            }
        }
        
        return messages;
    }
    
    /**
     * Convert message entity to DTO
     */
    public RedditMessageDto convertToDto(RedditMessage message) {
        RedditMessageDto dto = new RedditMessageDto();
        dto.setId(message.getId());
        dto.setRedditMessageId(message.getRedditMessageId());
        dto.setMessageType(message.getMessageType());
        dto.setSubject(message.getSubject());
        dto.setBody(message.getBody());
        dto.setAuthor(message.getAuthor());
        dto.setRecipient(message.getRecipient());
        dto.setSubreddit(message.getSubreddit());
        dto.setIsRead(message.getIsRead());
        dto.setRedditCreatedAt(message.getRedditCreatedAt());
        dto.setContext(message.getContext());
        dto.setParentId(message.getParentId());
        dto.setStoredAt(message.getStoredAt());
        
        return dto;
    }
    
    /**
     * Convert list of messages to DTOs
     */
    public List<RedditMessageDto> convertToDtoList(List<RedditMessage> messages) {
        List<RedditMessageDto> dtos = new ArrayList<>();
        for (RedditMessage message : messages) {
            dtos.add(convertToDto(message));
        }
        return dtos;
    }
    
    /**
     * Calculate token expiry time
     */
    public LocalDateTime calculateTokenExpiry(Integer expiresInSeconds) {
        return LocalDateTime.now().plusSeconds(expiresInSeconds);
    }
    
    /**
     * Check if token is expired
     */
    public boolean isTokenExpired(LocalDateTime expiryTime) {
        return expiryTime != null && expiryTime.isBefore(LocalDateTime.now());
    }
    
    /**
     * Clean HTML from message body
     */
    public String cleanHtmlFromBody(String htmlBody) {
        if (htmlBody == null) {
            return null;
        }
        
        return htmlBody
                .replaceAll("<[^>]+>", "") // Remove HTML tags
                .replaceAll("&amp;", "&")  // Replace HTML entities
                .replaceAll("&lt;", "<")
                .replaceAll("&gt;", ">")
                .replaceAll("&quot;", "\"")
                .replaceAll("&apos;", "'")
                .replaceAll("&#x27;", "'")
                .replaceAll("&#x2F;", "/")
                .trim();
    }
}
"""
        },

        {
            "path": "src\\main\\java\\com\\anuj\\redditmessagemanager\\util\\ValidationUtil.java",
            "content": """package com.anuj.redditmessagemanager.util;

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
"""
        },

        {
            "path": "src\\main\\java\\com\\anuj\\redditmessagemanager\\util\\DateTimeUtil.java",
            "content": """package com.anuj.redditmessagemanager.util;

import org.springframework.stereotype.Component;

import java.time.LocalDateTime;
import java.time.ZoneOffset;
import java.time.format.DateTimeFormatter;
import java.time.temporal.ChronoUnit;

@Component
public class DateTimeUtil {
    
    private static final DateTimeFormatter DISPLAY_FORMATTER = DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss");
    private static final DateTimeFormatter FILE_SAFE_FORMATTER = DateTimeFormatter.ofPattern("yyyy-MM-dd_HH-mm-ss");
    
    /**
     * Convert Unix timestamp to LocalDateTime
     */
    public LocalDateTime fromUnixTimestamp(Long timestamp) {
        if (timestamp == null) {
            return null;
        }
        return LocalDateTime.ofEpochSecond(timestamp, 0, ZoneOffset.UTC);
    }
    
    /**
     * Convert Unix timestamp (Double) to LocalDateTime
     */
    public LocalDateTime fromUnixTimestamp(Double timestamp) {
        if (timestamp == null) {
            return null;
        }
        return LocalDateTime.ofEpochSecond(timestamp.longValue(), 0, ZoneOffset.UTC);
    }
    
    /**
     * Convert LocalDateTime to Unix timestamp
     */
    public Long toUnixTimestamp(LocalDateTime dateTime) {
        if (dateTime == null) {
            return null;
        }
        return dateTime.toEpochSecond(ZoneOffset.UTC);
    }
    
    /**
     * Format DateTime for display
     */
    public String formatForDisplay(LocalDateTime dateTime) {
        if (dateTime == null) {
            return "N/A";
        }
        return dateTime.format(DISPLAY_FORMATTER);
    }
    
    /**
     * Format DateTime for filename
     */
    public String formatForFilename(LocalDateTime dateTime) {
        if (dateTime == null) {
            return "unknown";
        }
        return dateTime.format(FILE_SAFE_FORMATTER);
    }
    
    /**
     * Get relative time string
     */
    public String getRelativeTime(LocalDateTime dateTime) {
        if (dateTime == null) {
            return "Unknown time";
        }
        
        LocalDateTime now = LocalDateTime.now();
        long minutes = ChronoUnit.MINUTES.between(dateTime, now);
        long hours = ChronoUnit.HOURS.between(dateTime, now);
        long days = ChronoUnit.DAYS.between(dateTime, now);
        
        if (minutes < 1) {
            return "Just now";
        } else if (minutes < 60) {
            return minutes + " minute" + (minutes == 1 ? "" : "s") + " ago";
        } else if (hours < 24) {
            return hours + " hour" + (hours == 1 ? "" : "s") + " ago";
        } else if (days < 7) {
            return days + " day" + (days == 1 ? "" : "s") + " ago";
        } else {
            return formatForDisplay(dateTime);
        }
    }
    
    /**
     * Check if DateTime is recent (within last hour)
     */
    public boolean isRecent(LocalDateTime dateTime) {
        if (dateTime == null) {
            return false;
        }
        return ChronoUnit.HOURS.between(dateTime, LocalDateTime.now()) <= 1;
    }
    
    /**
     * Check if DateTime is today
     */
    public boolean isToday(LocalDateTime dateTime) {
        if (dateTime == null) {
            return false;
        }
        return dateTime.toLocalDate().equals(LocalDateTime.now().toLocalDate());
    }
    
    /**
     * Get start of day
     */
    public LocalDateTime getStartOfDay(LocalDateTime dateTime) {
        if (dateTime == null) {
            return null;
        }
        return dateTime.truncatedTo(ChronoUnit.DAYS);
    }
    
    /**
     * Get end of day
     */
    public LocalDateTime getEndOfDay(LocalDateTime dateTime) {
        if (dateTime == null) {
            return null;
        }
        return dateTime.truncatedTo(ChronoUnit.DAYS).plusDays(1).minusNanos(1);
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

    # Create all files
    create_files(config_files, "Configuration")
    create_files(dto_files, "DTO")
    create_files(util_files, "Utility")

    print("\n" + "="*70)
    print("Config, DTO, and Util classes created successfully!")
    print("="*70)

    print("\nCreated Configuration Classes:")
    print("✓ RedditConfig.java - Reddit API configuration and beans")
    print("✓ WebConfig.java - Web MVC configuration")
    print("✓ SecurityConfig.java - Security configuration")

    print("\nCreated DTO Classes:")
    print("✓ RedditTokenResponse.java - OAuth token response")
    print("✓ RedditMessageDto.java - Message data transfer object")
    print("✓ UserDto.java - User data transfer object")
    print("✓ RedditApiMessageResponse.java - Reddit API response mapping")
    print("✓ SearchResultDto.java - Search results wrapper")

    print("\nCreated Utility Classes:")
    print("✓ RedditApiUtil.java - Reddit API helper methods")
    print("✓ ValidationUtil.java - Input validation utilities")
    print("✓ DateTimeUtil.java - Date/time conversion utilities")

    print("\nFeatures included:")
    print("• OAuth2 configuration with your Reddit credentials")
    print("• Security configuration for protected endpoints")
    print("• Complete DTO mappings for Reddit API responses")
    print("• Utility methods for API integration")
    print("• Input validation and sanitization")
    print("• Date/time conversion helpers")
    print("• Web configuration for static resources")

    print("\nNext steps:")
    print("1. Create service classes")
    print("2. Create controller classes")
    print("3. Test the configuration")
    print("4. Run the application")

if __name__ == "__main__":
    create_config_dto_util_code()
