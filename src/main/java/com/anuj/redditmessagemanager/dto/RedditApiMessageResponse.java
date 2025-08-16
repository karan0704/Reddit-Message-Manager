package com.anuj.redditmessagemanager.dto;

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
