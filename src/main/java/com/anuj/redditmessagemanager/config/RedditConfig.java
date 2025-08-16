package com.anuj.redditmessagemanager.config;

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
