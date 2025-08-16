package com.anuj.redditmessagemanager.entity;

import jakarta.persistence.*;
import lombok.Data;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;
import org.hibernate.annotations.CreationTimestamp;

import java.time.LocalDateTime;

@Entity
@Table(name = "search_history")
@Data
@NoArgsConstructor
@AllArgsConstructor
public class SearchHistory {
    
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    @Column(name = "search_query", nullable = false)
    private String searchQuery;
    
    @Column(name = "search_type")
    @Enumerated(EnumType.STRING)
    private SearchType searchType;
    
    @Column(name = "results_count")
    private Integer resultsCount;
    
    @CreationTimestamp
    @Column(name = "searched_at")
    private LocalDateTime searchedAt;
    
    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "user_id", nullable = false)
    private User user;
    
    public enum SearchType {
        MESSAGES,
        USERS, 
        CHATS,
        POSTS
    }
    
    public SearchHistory(String searchQuery, SearchType searchType, Integer resultsCount, User user) {
        this.searchQuery = searchQuery;
        this.searchType = searchType;
        this.resultsCount = resultsCount;
        this.user = user;
    }
}
