package com.anuj.redditmessagemanager.dto;

import com.fasterxml.jackson.annotation.JsonProperty;
import lombok.Data;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;

import java.time.LocalDateTime;
import java.util.List;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class FilterDto {
    
    @JsonProperty("date_from")
    private LocalDateTime dateFrom;
    
    @JsonProperty("date_to")
    private LocalDateTime dateTo;
    
    @JsonProperty("username_filter")
    private String usernameFilter;
    
    @JsonProperty("username_starts_with")
    private String usernameStartsWith;
    
    @JsonProperty("username_contains")
    private String usernameContains;
    
    @JsonProperty("message_content_filter")
    private String messageContentFilter;
    
    @JsonProperty("only_pinned")
    private Boolean onlyPinned;
    
    @JsonProperty("only_unread")
    private Boolean onlyUnread;
    
    @JsonProperty("only_with_images")
    private Boolean onlyWithImages;
    
    @JsonProperty("exclude_blocked")
    private Boolean excludeBlocked;
    
    @JsonProperty("chat_ids")
    private List<Long> chatIds; // For specific chat filtering
    
    @JsonProperty("user_ids")
    private List<Long> userIds; // For specific user filtering
    
    @JsonProperty("sort_by")
    private String sortBy; // "recent", "oldest", "username", "message_count"
    
    @JsonProperty("sort_direction")
    private String sortDirection; // "asc", "desc"
    
    @JsonProperty("page")
    private Integer page = 0;
    
    @JsonProperty("page_size")
    private Integer pageSize = 20;
    
    // Constructor for date range filtering
    public FilterDto(LocalDateTime dateFrom, LocalDateTime dateTo) {
        this.dateFrom = dateFrom;
        this.dateTo = dateTo;
        this.onlyPinned = false;
        this.onlyUnread = false;
        this.excludeBlocked = true;
        this.sortBy = "recent";
        this.sortDirection = "desc";
    }
    
    // Constructor for username filtering
    public FilterDto(String usernameFilter, Boolean onlyUnread) {
        this.usernameFilter = usernameFilter;
        this.onlyUnread = onlyUnread;
        this.excludeBlocked = true;
        this.sortBy = "recent";
        this.sortDirection = "desc";
    }
}
