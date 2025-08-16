package com.anuj.redditmessagemanager.dto;

import com.anuj.redditmessagemanager.entity.SearchHistory.SearchType;
import com.fasterxml.jackson.annotation.JsonProperty;
import lombok.Data;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;

import java.util.List;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class SearchResultDto {
    
    @JsonProperty("search_query")
    private String searchQuery;
    
    @JsonProperty("search_type")
    private SearchType searchType;
    
    @JsonProperty("total_results")
    private Integer totalResults;
    
    @JsonProperty("page")
    private Integer page;
    
    @JsonProperty("page_size")
    private Integer pageSize;
    
    @JsonProperty("has_more")
    private Boolean hasMore;
    
    // Different result types
    private List<MessageDto> messages;
    private List<ChatDto> chats;
    private List<UserDto> users;
    
    @JsonProperty("search_time_ms")
    private Long searchTimeMs;
    
    @JsonProperty("highlighted_terms")
    private List<String> highlightedTerms;
    
    @JsonProperty("suggestions")
    private List<String> suggestions;
    
    // Constructor for message search results
    public SearchResultDto(String searchQuery, List<MessageDto> messages, Integer totalResults) {
        this.searchQuery = searchQuery;
        this.searchType = SearchType.MESSAGES;
        this.messages = messages;
        this.totalResults = totalResults;
        this.page = 0;
        this.pageSize = messages != null ? messages.size() : 0;
        this.hasMore = false;
    }
    
    // Constructor for user search results
    public SearchResultDto(String searchQuery, List<UserDto> users) {
        this.searchQuery = searchQuery;
        this.searchType = SearchType.USERS;
        this.users = users;
        this.totalResults = users != null ? users.size() : 0;
    }
    
    // Constructor for chat search results
    public SearchResultDto(String searchQuery, List<ChatDto> chats) {
        this.searchQuery = searchQuery;
        this.searchType = SearchType.POSTS; // Reusing existing enum value
        this.chats = chats;
        this.totalResults = chats != null ? chats.size() : 0;
    }
}
