package com.anuj.redditmessagemanager.repository;

import com.anuj.redditmessagemanager.entity.SearchHistory;
import com.anuj.redditmessagemanager.entity.SearchHistory.SearchType;
import com.anuj.redditmessagemanager.entity.User;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.time.LocalDateTime;
import java.util.List;

@Repository
public interface SearchHistoryRepository extends JpaRepository<SearchHistory, Long> {
    
    /**
     * Find search history by user
     */
    List<SearchHistory> findByUserOrderBySearchedAtDesc(User user);
    
    /**
     * Find recent searches by user (last 10)
     */
    List<SearchHistory> findTop10ByUserOrderBySearchedAtDesc(User user);
    
    /**
     * Find search history by user and type
     */
    List<SearchHistory> findByUserAndSearchTypeOrderBySearchedAtDesc(User user, SearchType searchType);
    
    /**
     * Find searches by query
     */
    List<SearchHistory> findByUserAndSearchQueryContainingIgnoreCaseOrderBySearchedAtDesc(User user, String query);
    
    /**
     * Find searches within date range
     */
    List<SearchHistory> findByUserAndSearchedAtBetweenOrderBySearchedAtDesc(User user, 
                                                                            LocalDateTime startDate, 
                                                                            LocalDateTime endDate);
    
    /**
     * Get most popular search terms for user
     */
    @Query("SELECT s.searchQuery, COUNT(s) as searchCount FROM SearchHistory s " +
           "WHERE s.user = :user " +
           "GROUP BY s.searchQuery " +
           "ORDER BY searchCount DESC")
    List<Object[]> findMostPopularSearchTerms(@Param("user") User user);
    
    /**
     * Get recent unique search terms for autocomplete
     */
    @Query("SELECT DISTINCT s.searchQuery FROM SearchHistory s WHERE s.user = :user " +
           "AND LOWER(s.searchQuery) LIKE LOWER(CONCAT(:prefix, '%')) " +
           "ORDER BY s.searchedAt DESC")
    List<String> findRecentSearchTermsForAutocomplete(@Param("user") User user, @Param("prefix") String prefix);
    
    /**
     * Count searches by user
     */
    long countByUser(User user);
    
    /**
     * Count searches by type for user
     */
    long countByUserAndSearchType(User user, SearchType searchType);
    
    /**
     * Delete old search history (older than specified date)
     */
    void deleteByUserAndSearchedAtBefore(User user, LocalDateTime cutoffDate);
    
    /**
     * Find searches with results
     */
    List<SearchHistory> findByUserAndResultsCountGreaterThanOrderBySearchedAtDesc(User user, Integer minResults);
    
    /**
     * Check if search query exists for user
     */
    boolean existsByUserAndSearchQuery(User user, String searchQuery);
    
    /**
     * Find similar search queries
     */
    @Query("SELECT s FROM SearchHistory s WHERE s.user = :user " +
           "AND LOWER(s.searchQuery) LIKE LOWER(CONCAT('%', :searchTerm, '%')) " +
           "AND s.searchQuery != :exactQuery ORDER BY s.searchedAt DESC")
    List<SearchHistory> findSimilarSearches(@Param("user") User user, 
                                           @Param("searchTerm") String searchTerm,
                                           @Param("exactQuery") String exactQuery);
    
    /**
     * Get search statistics for user
     */
    @Query("SELECT s.searchType, COUNT(s), AVG(s.resultsCount) FROM SearchHistory s " +
           "WHERE s.user = :user GROUP BY s.searchType")
    List<Object[]> getSearchStatistics(@Param("user") User user);
}
