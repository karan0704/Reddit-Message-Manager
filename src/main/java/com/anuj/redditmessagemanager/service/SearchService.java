package com.anuj.redditmessagemanager.service;

import com.anuj.redditmessagemanager.dto.SearchResultDto;
import com.anuj.redditmessagemanager.dto.FilterDto;
import com.anuj.redditmessagemanager.dto.UserDto;
import com.anuj.redditmessagemanager.dto.ChatDto;
import com.anuj.redditmessagemanager.entity.SearchHistory;
import com.anuj.redditmessagemanager.entity.SearchHistory.SearchType;
import com.anuj.redditmessagemanager.entity.User;
import com.anuj.redditmessagemanager.repository.SearchHistoryRepository;
import com.anuj.redditmessagemanager.util.ValidationUtil;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.time.LocalDateTime;
import java.util.List;
import java.util.stream.Collectors;

@Service
@Transactional
public class SearchService {
    
    private static final Logger logger = LoggerFactory.getLogger(SearchService.class);
    
    @Autowired
    private SearchHistoryRepository searchHistoryRepository;
    
    @Autowired
    private MessageService messageService;
    
    @Autowired
    private UserService userService;
    
    @Autowired
    private ChatService chatService;
    
    @Autowired
    private ValidationUtil validationUtil;
    
    /**
     * Search messages by content
     */
    public SearchResultDto searchMessages(String username, String query, Long chatId) {
        try {
            long startTime = System.currentTimeMillis();
            
            String sanitizedQuery = validationUtil.sanitizeSearchQuery(query);
            
            var messages = messageService.searchMessages(username, sanitizedQuery, chatId);
            
            // Save search history
            User user = userService.findByUsername(username);
            if (user != null) {
                saveSearchHistory(user, sanitizedQuery, SearchType.MESSAGES, messages.size());
            }
            
            long searchTime = System.currentTimeMillis() - startTime;
            
            SearchResultDto result = new SearchResultDto();
            result.setSearchQuery(sanitizedQuery);
            result.setSearchType(SearchType.MESSAGES);
            result.setMessages(messages);
            result.setTotalResults(messages.size());
            result.setSearchTimeMs(searchTime);
            
            logger.info("Message search completed for user {}: {} results in {}ms", 
                username, messages.size(), searchTime);
            
            return result;
            
        } catch (Exception e) {
            logger.error("Error searching messages: {}", e.getMessage());
            throw new RuntimeException("Message search failed", e);
        }
    }
    
    /**
     * Search users by username or display name
     */
    public SearchResultDto searchUsers(String currentUsername, String query) {
        try {
            long startTime = System.currentTimeMillis();
            
            List<UserDto> users = userService.searchUsers(query, currentUsername);
            
            // Save search history
            User user = userService.findByUsername(currentUsername);
            if (user != null) {
                saveSearchHistory(user, query, SearchType.USERS, users.size());
            }
            
            long searchTime = System.currentTimeMillis() - startTime;
            
            SearchResultDto result = new SearchResultDto();
            result.setSearchQuery(query);
            result.setSearchType(SearchType.USERS);
            result.setUsers(users);
            result.setTotalResults(users.size());
            result.setSearchTimeMs(searchTime);
            
            logger.info("User search completed for {}: {} results in {}ms", 
                currentUsername, users.size(), searchTime);
            
            return result;
            
        } catch (Exception e) {
            logger.error("Error searching users: {}", e.getMessage());
            throw new RuntimeException("User search failed", e);
        }
    }
    
    /**
     * Search chats by other user's username
     */
    public SearchResultDto searchChats(String username, String query) {
        try {
            long startTime = System.currentTimeMillis();
            
            // Get all user chats and filter by query
            List<ChatDto> allChats = chatService.getUserChats(username);
            List<ChatDto> filteredChats = allChats.stream()
                    .filter(chat -> chat.getOtherUsername() != null && 
                                  chat.getOtherUsername().toLowerCase().contains(query.toLowerCase()))
                    .collect(Collectors.toList());
            
            // Save search history
            User user = userService.findByUsername(username);
            if (user != null) {
                saveSearchHistory(user, query, SearchType.POSTS, filteredChats.size()); // Reuse POSTS enum
            }
            
            long searchTime = System.currentTimeMillis() - startTime;
            
            SearchResultDto result = new SearchResultDto();
            result.setSearchQuery(query);
            result.setSearchType(SearchType.POSTS);
            result.setChats(filteredChats);
            result.setTotalResults(filteredChats.size());
            result.setSearchTimeMs(searchTime);
            
            logger.info("Chat search completed for user {}: {} results in {}ms", 
                username, filteredChats.size(), searchTime);
            
            return result;
            
        } catch (Exception e) {
            logger.error("Error searching chats: {}", e.getMessage());
            throw new RuntimeException("Chat search failed", e);
        }
    }
    
    /**
     * Advanced search with filters
     */
    public SearchResultDto advancedSearch(String username, FilterDto filter) {
        try {
            long startTime = System.currentTimeMillis();
            
            SearchResultDto result = new SearchResultDto();
            result.setSearchQuery(filter.getMessageContentFilter());
            result.setSearchType(SearchType.MESSAGES);
            result.setPage(filter.getPage());
            result.setPageSize(filter.getPageSize());
            
            // Apply various filters
            var messages = messageService.searchMessages(username, 
                filter.getMessageContentFilter() != null ? filter.getMessageContentFilter() : "", 
                null);
            
            // Additional filtering based on filter criteria
            if (filter.getDateFrom() != null || filter.getDateTo() != null) {
                messages = messages.stream()
                        .filter(msg -> {
                            if (filter.getDateFrom() != null && msg.getCreatedAt().isBefore(filter.getDateFrom())) {
                                return false;
                            }
                            if (filter.getDateTo() != null && msg.getCreatedAt().isAfter(filter.getDateTo())) {
                                return false;
                            }
                            return true;
                        })
                        .collect(Collectors.toList());
            }
            
            result.setMessages(messages);
            result.setTotalResults(messages.size());
            result.setSearchTimeMs(System.currentTimeMillis() - startTime);
            
            // Save search history
            User user = userService.findByUsername(username);
            if (user != null && filter.getMessageContentFilter() != null) {
                saveSearchHistory(user, filter.getMessageContentFilter(), SearchType.MESSAGES, messages.size());
            }
            
            logger.info("Advanced search completed for user {}: {} results", username, messages.size());
            
            return result;
            
        } catch (Exception e) {
            logger.error("Error in advanced search: {}", e.getMessage());
            throw new RuntimeException("Advanced search failed", e);
        }
    }
    
    /**
     * Get autocomplete suggestions
     */
    public List<String> getAutocompleteSuggestions(String username, String query, String type) {
        try {
            User user = userService.findByUsername(username);
            if (user == null) {
                return List.of();
            }
            
            switch (type.toLowerCase()) {
                case "search":
                    return searchHistoryRepository.findRecentSearchTermsForAutocomplete(user, query);
                
                case "users":
                    return userService.getUsernameAutocomplete(query, username).stream()
                            .map(UserDto::getUsername)
                            .collect(Collectors.toList());
                
                default:
                    return searchHistoryRepository.findRecentSearchTermsForAutocomplete(user, query);
            }
            
        } catch (Exception e) {
            logger.error("Error getting autocomplete suggestions: {}", e.getMessage());
            return List.of();
        }
    }
    
    /**
     * Get search history for user
     */
    public List<SearchHistory> getSearchHistory(String username) {
        try {
            User user = userService.findByUsername(username);
            if (user == null) {
                return List.of();
            }
            
            return searchHistoryRepository.findTop10ByUserOrderBySearchedAtDesc(user);
            
        } catch (Exception e) {
            logger.error("Error getting search history: {}", e.getMessage());
            return List.of();
        }
    }
    
    /**
     * Clear search history for user
     */
    public void clearSearchHistory(String username) {
        try {
            User user = userService.findByUsername(username);
            if (user != null) {
                List<SearchHistory> userSearches = searchHistoryRepository.findByUserOrderBySearchedAtDesc(user);
                searchHistoryRepository.deleteAll(userSearches);
                
                logger.info("Search history cleared for user: {}", username);
            }
        } catch (Exception e) {
            logger.error("Error clearing search history: {}", e.getMessage());
            throw new RuntimeException("Failed to clear search history", e);
        }
    }
    
    /**
     * Get popular search terms for user
     */
    public List<String> getPopularSearchTerms(String username) {
        try {
            User user = userService.findByUsername(username);
            if (user == null) {
                return List.of();
            }
            
            List<Object[]> popularTerms = searchHistoryRepository.findMostPopularSearchTerms(user);
            
            return popularTerms.stream()
                    .limit(10)
                    .map(result -> (String) result[0])
                    .collect(Collectors.toList());
                    
        } catch (Exception e) {
            logger.error("Error getting popular search terms: {}", e.getMessage());
            return List.of();
        }
    }
    
    /**
     * Save search history entry
     */
    private void saveSearchHistory(User user, String query, SearchType searchType, Integer resultsCount) {
        try {
            // Don't save empty queries or duplicates within short time
            if (query.trim().length() < 2) {
                return;
            }
            
            SearchHistory searchHistory = new SearchHistory(query, searchType, resultsCount, user);
            searchHistoryRepository.save(searchHistory);
            
        } catch (Exception e) {
            logger.warn("Failed to save search history: {}", e.getMessage());
            // Don't throw exception as this is not critical
        }
    }
}
