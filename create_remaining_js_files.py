import os

def create_remaining_js_files():
    # Base path from your previous conversation
    base_path = "D:\\Karan Ticket Project\\Reddit Message Manager"
    
    # Remaining JavaScript files for the local chat application
    remaining_js_files = [
        {
            "path": "src\\main\\resources\\static\\js\\search.js",
            "content": r"""// Search functionality
console.log('Search module loaded');

// Search-related variables
let searchTimeout = null;
let searchHistory = [];
let currentSearchResults = [];
let searchSuggestions = [];

/**
 * Perform search
 */
async function performSearch(query, type = 'all') {
    if (!query || query.trim().length < 2) {
        clearSearchResults();
        return;
    }
    
    try {
        showSearchLoading();
        
        let endpoint = '';
        let params = new URLSearchParams({ q: query.trim() });
        
        switch (type) {
            case 'messages':
                endpoint = '/api/search/messages';
                break;
            case 'users':
                endpoint = '/api/search/users';
                break;
            case 'chats':
                endpoint = '/api/search/chats';
                break;
            default:
                endpoint = '/api/search/messages';
        }
        
        const response = await fetch(`${CONFIG.API_BASE_URL}${endpoint}?${params}`);
        const data = await response.json();
        
        if (response.ok) {
            currentSearchResults = data;
            displaySearchResults(data, type);
            addToSearchHistory(query, type);
        } else {
            throw new Error(data.error || 'Search failed');
        }
        
    } catch (error) {
        console.error('Search error:', error);
        showSearchError('Search failed. Please try again.');
    }
}

/**
 * Display search results
 */
function displaySearchResults(results, searchType) {
    const resultsContainer = document.getElementById('searchResults');
    const resultsContent = document.getElementById('searchResultsContent');
    
    if (!resultsContainer || !resultsContent) {
        console.warn('Search results container not found');
        return;
    }
    
    resultsContainer.classList.remove('hidden');
    
    if (!results || (!results.messages && !results.users && !results.chats)) {
        resultsContent.innerHTML = `
            <div class="no-results">
                <h4>No results found</h4>
                <p>Try adjusting your search query or filters.</p>
            </div>
        `;
        return;
    }
    
    let html = '';
    
    // Display messages
    if (results.messages && results.messages.length > 0) {
        html += `<div class="search-section">
            <h4>Messages (${results.messages.length})</h4>
            <div class="search-results-list">
                ${results.messages.map(message => createMessageResultHtml(message)).join('')}
            </div>
        </div>`;
    }
    
    // Display users
    if (results.users && results.users.length > 0) {
        html += `<div class="search-section">
            <h4>Users (${results.users.length})</h4>
            <div class="search-results-list">
                ${results.users.map(user => createUserResultHtml(user)).join('')}
            </div>
        </div>`;
    }
    
    // Display chats
    if (results.chats && results.chats.length > 0) {
        html += `<div class="search-section">
            <h4>Chats (${results.chats.length})</h4>
            <div class="search-results-list">
                ${results.chats.map(chat => createChatResultHtml(chat)).join('')}
            </div>
        </div>`;
    }
    
    resultsContent.innerHTML = html;
}

/**
 * Create message result HTML
 */
function createMessageResultHtml(message) {
    const preview = message.messageContent.length > 100 ? 
        message.messageContent.substring(0, 100) + '...' : message.messageContent;
    
    return `
        <div class="search-result-item message-result" data-message-id="${message.id}" data-chat-id="${message.chatId}">
            <div class="result-icon">📝</div>
            <div class="result-content">
                <div class="result-title">Message from ${escapeHtml(message.senderUsername)}</div>
                <div class="result-preview">${escapeHtml(preview)}</div>
                <div class="result-meta">
                    <span>${formatDate(message.createdAt)}</span>
                    ${message.chatId ? ` • <span onclick="openChatFromSearch(${message.chatId})">Open Chat</span>` : ''}
                </div>
            </div>
            <div class="result-actions">
                <button onclick="openChatFromSearch(${message.chatId}, ${message.id})" class="btn btn-small btn-primary">
                    View
                </button>
            </div>
        </div>
    `;
}

/**
 * Create user result HTML
 */
function createUserResultHtml(user) {
    return `
        <div class="search-result-item user-result" data-username="${user.username}">
            <div class="result-avatar">
                <img src="/api/user/${encodeURIComponent(user.username)}/avatar" 
                     alt="${escapeHtml(user.username)}" class="avatar-img"
                     onerror="this.src='/images/default-avatar.png'">
            </div>
            <div class="result-content">
                <div class="result-title">${escapeHtml(user.displayName || user.username)}</div>
                <div class="result-subtitle">@${escapeHtml(user.username)}</div>
                <div class="result-meta">
                    <span class="${user.isOnline ? 'online-status' : 'offline-status'}">
                        ${user.isOnline ? 'Online' : 'Offline'}
                    </span>
                </div>
            </div>
            <div class="result-actions">
                <button onclick="startChatFromSearch('${escapeHtml(user.username)}')" class="btn btn-small btn-primary">
                    Chat
                </button>
            </div>
        </div>
    `;
}

/**
 * Clear search results
 */
function clearSearchResults() {
    const resultsContainer = document.getElementById('searchResults');
    const resultsContent = document.getElementById('searchResultsContent');
    
    if (resultsContainer) {
        resultsContainer.classList.add('hidden');
    }
    
    if (resultsContent) {
        resultsContent.innerHTML = '';
    }
    
    currentSearchResults = [];
}

/**
 * Show search loading
 */
function showSearchLoading() {
    const resultsContainer = document.getElementById('searchResults');
    const resultsContent = document.getElementById('searchResultsContent');
    
    if (resultsContainer) {
        resultsContainer.classList.remove('hidden');
    }
    
    if (resultsContent) {
        resultsContent.innerHTML = `
            <div class="loading">
                <div class="spinner"></div>
                <span>Searching...</span>
            </div>
        `;
    }
}

/**
 * Show search error
 */
function showSearchError(message) {
    const resultsContent = document.getElementById('searchResultsContent');
    
    if (resultsContent) {
        resultsContent.innerHTML = `
            <div class="error-message">
                <h4>Search Failed</h4>
                <p>${escapeHtml(message)}</p>
                <button onclick="clearSearchResults()" class="btn btn-primary">Close</button>
            </div>
        `;
    }
}

/**
 * Add query to search history
 */
function addToSearchHistory(query, type) {
    const historyItem = {
        query: query,
        type: type,
        timestamp: Date.now()
    };
    
    searchHistory = searchHistory.filter(item => 
        !(item.query === query && item.type === type)
    );
    
    searchHistory.unshift(historyItem);
    
    if (searchHistory.length > 50) {
        searchHistory = searchHistory.slice(0, 50);
    }
    
    try {
        localStorage.setItem('searchHistory', JSON.stringify(searchHistory));
    } catch (error) {
        console.warn('Failed to save search history:', error);
    }
}

// Export search functions
window.ChatApp = {
    ...window.ChatApp,
    performSearch,
    clearSearchResults,
    displaySearchResults
};

console.log('Search module loaded successfully');
"""
        },
        
        {
            "path": "src\\main\\resources\\static\\js\\filters.js",
            "content": r"""// Filter functionality
console.log('Filters module loaded');

// Filter state
let currentFilters = {
    dateFrom: null,
    dateTo: null,
    users: [],
    messageTypes: ['TEXT', 'IMAGE', 'FILE'],
    status: 'all',
    chatStatus: {
        pinned: false,
        archived: false
    },
    sortBy: 'recent'
};

/**
 * Initialize filters
 */
function initializeFilters() {
    loadSavedFilters();
    setupFilterEventListeners();
}

/**
 * Setup filter event listeners
 */
function setupFilterEventListeners() {
    // Date filters
    const dateFromInput = document.getElementById('filterDateFrom');
    const dateToInput = document.getElementById('filterDateTo');
    
    if (dateFromInput) {
        dateFromInput.addEventListener('change', updateDateFilter);
    }
    
    if (dateToInput) {
        dateToInput.addEventListener('change', updateDateFilter);
    }
    
    // Message type checkboxes
    document.querySelectorAll('input[name="messageType"]').forEach(checkbox => {
        checkbox.addEventListener('change', updateMessageTypeFilter);
    });
    
    // Status radio buttons
    document.querySelectorAll('input[name="statusFilter"]').forEach(radio => {
        radio.addEventListener('change', updateStatusFilter);
    });
    
    // Sort dropdown
    const sortSelect = document.getElementById('sortBy');
    if (sortSelect) {
        sortSelect.addEventListener('change', updateSortFilter);
    }
}

/**
 * Toggle filters panel
 */
function toggleFilters() {
    const filtersPanel = document.getElementById('filtersPanel');
    if (filtersPanel) {
        filtersPanel.classList.toggle('hidden');
    }
}

/**
 * Apply filters to current view
 */
function applyFilters() {
    const filteredData = filterData(getCurrentData(), currentFilters);
    displayFilteredData(filteredData);
    saveFiltersToStorage();
    showNotification('Filters applied', 'success', 1500);
}

/**
 * Clear all filters
 */
function clearFilters() {
    currentFilters = {
        dateFrom: null,
        dateTo: null,
        users: [],
        messageTypes: ['TEXT', 'IMAGE', 'FILE'],
        status: 'all',
        chatStatus: {
            pinned: false,
            archived: false
        },
        sortBy: 'recent'
    };
    
    updateFilterUI();
    applyFilters();
    showNotification('Filters cleared', 'info', 1500);
}

/**
 * Update date filter
 */
function updateDateFilter() {
    const dateFromInput = document.getElementById('filterDateFrom');
    const dateToInput = document.getElementById('filterDateTo');
    
    currentFilters.dateFrom = dateFromInput?.value ? new Date(dateFromInput.value) : null;
    currentFilters.dateTo = dateToInput?.value ? new Date(dateToInput.value) : null;
    
    // Validate date range
    if (currentFilters.dateFrom && currentFilters.dateTo && 
        currentFilters.dateFrom > currentFilters.dateTo) {
        showNotification('Start date cannot be after end date', 'error');
        return;
    }
    
    applyFilters();
}

/**
 * Update message type filter
 */
function updateMessageTypeFilter() {
    const checkboxes = document.querySelectorAll('input[name="messageType"]:checked');
    currentFilters.messageTypes = Array.from(checkboxes).map(cb => cb.value);
    applyFilters();
}

/**
 * Update status filter
 */
function updateStatusFilter() {
    const selectedStatus = document.querySelector('input[name="statusFilter"]:checked');
    currentFilters.status = selectedStatus ? selectedStatus.value : 'all';
    applyFilters();
}

/**
 * Update sort filter
 */
function updateSortFilter() {
    const sortSelect = document.getElementById('sortBy');
    currentFilters.sortBy = sortSelect ? sortSelect.value : 'recent';
    applyFilters();
}

/**
 * Add user filter
 */
function addUserFilter(username) {
    if (!currentFilters.users.includes(username)) {
        currentFilters.users.push(username);
        updateUserFilterUI();
        applyFilters();
    }
}

/**
 * Remove user filter
 */
function removeUserFilter(username) {
    currentFilters.users = currentFilters.users.filter(user => user !== username);
    updateUserFilterUI();
    applyFilters();
}

/**
 * Update user filter UI
 */
function updateUserFilterUI() {
    const selectedUsersContainer = document.getElementById('selectedUsers');
    if (!selectedUsersContainer) return;
    
    selectedUsersContainer.innerHTML = currentFilters.users.map(username => `
        <div class="user-tag" data-username="${username}">
            <span class="user-tag-name">${escapeHtml(username)}</span>
            <button onclick="removeUserFilter('${username}')" class="remove-tag-btn">×</button>
        </div>
    `).join('');
}

/**
 * Filter data based on current filters
 */
function filterData(data, filters) {
    if (!data || !Array.isArray(data)) return data;
    
    return data.filter(item => {
        // Date filter
        if (filters.dateFrom || filters.dateTo) {
            const itemDate = new Date(item.createdAt || item.timestamp || item.lastMessageTimestamp);
            
            if (filters.dateFrom && itemDate < filters.dateFrom) return false;
            if (filters.dateTo && itemDate > filters.dateTo) return false;
        }
        
        // User filter
        if (filters.users.length > 0) {
            const itemUser = item.senderUsername || item.username || item.otherUsername;
            if (!filters.users.includes(itemUser)) return false;
        }
        
        // Message type filter
        if (item.messageType && !filters.messageTypes.includes(item.messageType)) {
            return false;
        }
        
        // Status filter
        if (filters.status !== 'all') {
            if (filters.status === 'read' && !item.isRead) return false;
            if (filters.status === 'unread' && item.isRead) return false;
        }
        
        // Chat status filter
        if (filters.chatStatus.pinned && !item.isPinned) return false;
        if (!filters.chatStatus.archived && item.isArchived) return false;
        
        return true;
    }).sort((a, b) => {
        // Apply sorting
        switch (filters.sortBy) {
            case 'recent':
                const dateA = new Date(a.createdAt || a.lastMessageTimestamp || 0);
                const dateB = new Date(b.createdAt || b.lastMessageTimestamp || 0);
                return dateB - dateA;
                
            case 'oldest':
                const oldDateA = new Date(a.createdAt || a.lastMessageTimestamp || 0);
                const oldDateB = new Date(b.createdAt || b.lastMessageTimestamp || 0);
                return oldDateA - oldDateB;
                
            case 'username':
                const userA = (a.senderUsername || a.username || a.otherUsername || '').toLowerCase();
                const userB = (b.senderUsername || b.username || b.otherUsername || '').toLowerCase();
                return userA.localeCompare(userB);
                
            case 'username_desc':
                const userDescA = (a.senderUsername || a.username || a.otherUsername || '').toLowerCase();
                const userDescB = (b.senderUsername || b.username || b.otherUsername || '').toLowerCase();
                return userDescB.localeCompare(userDescA);
                
            case 'message_count':
                return (b.messageCount || 0) - (a.messageCount || 0);
                
            default:
                return 0;
        }
    });
}

/**
 * Get current data to filter
 */
function getCurrentData() {
    // Return current chats or messages depending on active view
    if (currentSearchResults && currentSearchResults.length > 0) {
        return currentSearchResults;
    }
    
    // Get chats from DOM
    const chatElements = document.querySelectorAll('.chat-item');
    return Array.from(chatElements).map(el => ({
        id: parseInt(el.dataset.chatId),
        otherUsername: el.querySelector('.chat-username')?.textContent,
        lastMessage: el.querySelector('.last-message')?.textContent,
        lastMessageTimestamp: el.querySelector('.chat-time')?.textContent,
        isPinned: el.querySelector('.pinned-indicator') !== null,
        hasUnread: el.querySelector('.unread-indicator') !== null
    }));
}

/**
 * Display filtered data
 */
function displayFilteredData(filteredData) {
    // This would depend on current view - chats, messages, etc.
    console.log('Displaying filtered data:', filteredData);
    
    // If in chat list view
    const chatList = document.getElementById('chatList');
    if (chatList && filteredData) {
        // Hide/show chat items based on filter results
        const allChatItems = chatList.querySelectorAll('.chat-item');
        
        allChatItems.forEach(item => {
            const chatId = parseInt(item.dataset.chatId);
            const shouldShow = filteredData.some(data => data.id === chatId);
            item.style.display = shouldShow ? 'flex' : 'none';
        });
    }
}

/**
 * Update filter UI to reflect current filters
 */
function updateFilterUI() {
    // Update date inputs
    const dateFromInput = document.getElementById('filterDateFrom');
    const dateToInput = document.getElementById('filterDateTo');
    
    if (dateFromInput) {
        dateFromInput.value = currentFilters.dateFrom ? 
            currentFilters.dateFrom.toISOString().split('T')[0] : '';
    }
    
    if (dateToInput) {
        dateToInput.value = currentFilters.dateTo ? 
            currentFilters.dateTo.toISOString().split('T')[0] : '';
    }
    
    // Update message type checkboxes
    document.querySelectorAll('input[name="messageType"]').forEach(checkbox => {
        checkbox.checked = currentFilters.messageTypes.includes(checkbox.value);
    });
    
    // Update status radio buttons
    const statusRadio = document.querySelector(`input[name="statusFilter"][value="${currentFilters.status}"]`);
    if (statusRadio) {
        statusRadio.checked = true;
    }
    
    // Update sort dropdown
    const sortSelect = document.getElementById('sortBy');
    if (sortSelect) {
        sortSelect.value = currentFilters.sortBy;
    }
    
    // Update user filter UI
    updateUserFilterUI();
}

/**
 * Set quick date range
 */
function setDateRange(range) {
    const now = new Date();
    let startDate = new Date();
    
    switch (range) {
        case 'today':
            startDate = new Date(now.getFullYear(), now.getMonth(), now.getDate());
            break;
        case 'week':
            startDate = new Date(now.getTime() - 7 * 24 * 60 * 60 * 1000);
            break;
        case 'month':
            startDate = new Date(now.getFullYear(), now.getMonth(), 1);
            break;
    }
    
    currentFilters.dateFrom = startDate;
    currentFilters.dateTo = now;
    
    updateFilterUI();
    applyFilters();
}

/**
 * Save filters to localStorage
 */
function saveFiltersToStorage() {
    try {
        const filtersToSave = {
            ...currentFilters,
            dateFrom: currentFilters.dateFrom ? currentFilters.dateFrom.toISOString() : null,
            dateTo: currentFilters.dateTo ? currentFilters.dateTo.toISOString() : null
        };
        localStorage.setItem('chatFilters', JSON.stringify(filtersToSave));
    } catch (error) {
        console.warn('Failed to save filters:', error);
    }
}

/**
 * Load saved filters
 */
function loadSavedFilters() {
    try {
        const saved = localStorage.getItem('chatFilters');
        if (saved) {
            const parsedFilters = JSON.parse(saved);
            currentFilters = {
                ...currentFilters,
                ...parsedFilters,
                dateFrom: parsedFilters.dateFrom ? new Date(parsedFilters.dateFrom) : null,
                dateTo: parsedFilters.dateTo ? new Date(parsedFilters.dateTo) : null
            };
            updateFilterUI();
        }
    } catch (error) {
        console.warn('Failed to load saved filters:', error);
    }
}

/**
 * Export current filter settings
 */
function exportFilterSettings() {
    const filterData = {
        filters: currentFilters,
        exportedAt: new Date().toISOString(),
        version: '1.0'
    };
    
    const blob = new Blob([JSON.stringify(filterData, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    
    const a = document.createElement('a');
    a.href = url;
    a.download = 'chat-filters.json';
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
    
    showNotification('Filter settings exported', 'success');
}

/**
 * Import filter settings
 */
function importFilterSettings(event) {
    const file = event.target.files[0];
    if (!file) return;
    
    const reader = new FileReader();
    reader.onload = function(e) {
        try {
            const filterData = JSON.parse(e.target.result);
            if (filterData.filters) {
                currentFilters = {
                    ...currentFilters,
                    ...filterData.filters,
                    dateFrom: filterData.filters.dateFrom ? new Date(filterData.filters.dateFrom) : null,
                    dateTo: filterData.filters.dateTo ? new Date(filterData.filters.dateTo) : null
                };
                updateFilterUI();
                applyFilters();
                showNotification('Filter settings imported', 'success');
            }
        } catch (error) {
            console.error('Failed to import filters:', error);
            showNotification('Failed to import filter settings', 'error');
        }
    };
    reader.readAsText(file);
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', initializeFilters);

// Export filter functions
window.ChatApp = {
    ...window.ChatApp,
    toggleFilters,
    applyFilters,
    clearFilters,
    setDateRange,
    addUserFilter,
    removeUserFilter,
    exportFilterSettings,
    importFilterSettings
};

console.log('Filters module loaded successfully');
"""
        },
        
        {
            "path": "src\\main\\resources\\static\\js\\autocomplete.js",
            "content": r"""// Autocomplete functionality
console.log('Autocomplete module loaded');

// Autocomplete state
let autocompleteCache = new Map();
let autocompleteTimeout = null;
let currentAutocompleteInput = null;
let currentSuggestions = [];

/**
 * Initialize autocomplete for an input field
 */
function initializeAutocomplete(inputElement, options = {}) {
    if (!inputElement) return;
    
    const defaultOptions = {
        minLength: 2,
        delay: 300,
        maxSuggestions: 10,
        source: 'users', // 'users', 'chats', 'history'
        onSelect: null,
        placeholder: 'Start typing...'
    };
    
    const config = { ...defaultOptions, ...options };
    
    // Set up input listeners
    inputElement.addEventListener('input', (e) => handleAutocompleteInput(e, config));
    inputElement.addEventListener('keydown', (e) => handleAutocompleteKeydown(e));
    inputElement.addEventListener('blur', (e) => hideAutocompleteSuggestions(e));
    inputElement.addEventListener('focus', (e) => handleAutocompleteFocus(e, config));
    
    // Store config on element
    inputElement.autocompleteConfig = config;
}

/**
 * Handle autocomplete input
 */
function handleAutocompleteInput(event, config) {
    const input = event.target;
    const query = input.value.trim();
    
    currentAutocompleteInput = input;
    
    // Clear previous timeout
    if (autocompleteTimeout) {
        clearTimeout(autocompleteTimeout);
    }
    
    if (query.length < config.minLength) {
        hideAutocompleteSuggestions();
        return;
    }
    
    // Debounce the search
    autocompleteTimeout = setTimeout(() => {
        fetchAutocompleteSuggestions(query, config);
    }, config.delay);
}

/**
 * Handle autocomplete keydown events
 */
function handleAutocompleteKeydown(event) {
    const suggestionsList = document.getElementById('autocompleteSuggestions');
    if (!suggestionsList || suggestionsList.classList.contains('hidden')) {
        return;
    }
    
    const suggestions = suggestionsList.querySelectorAll('.autocomplete-suggestion');
    const activeIndex = Array.from(suggestions).findIndex(s => s.classList.contains('active'));
    
    switch (event.key) {
        case 'ArrowDown':
            event.preventDefault();
            const nextIndex = Math.min(activeIndex + 1, suggestions.length - 1);
            setActiveSuggestion(suggestions, nextIndex);
            break;
            
        case 'ArrowUp':
            event.preventDefault();
            const prevIndex = Math.max(activeIndex - 1, 0);
            setActiveSuggestion(suggestions, prevIndex);
            break;
            
        case 'Enter':
            event.preventDefault();
            if (activeIndex >= 0 && suggestions[activeIndex]) {
                selectSuggestion(suggestions[activeIndex]);
            }
            break;
            
        case 'Escape':
            hideAutocompleteSuggestions();
            break;
    }
}

/**
 * Handle autocomplete focus
 */
function handleAutocompleteFocus(event, config) {
    const input = event.target;
    const query = input.value.trim();
    
    if (query.length >= config.minLength) {
        fetchAutocompleteSuggestions(query, config);
    }
}

/**
 * Fetch autocomplete suggestions
 */
async function fetchAutocompleteSuggestions(query, config) {
    try {
        // Check cache first
        const cacheKey = `${config.source}:${query}`;
        if (autocompleteCache.has(cacheKey)) {
            const cachedSuggestions = autocompleteCache.get(cacheKey);
            displayAutocompleteSuggestions(cachedSuggestions, config);
            return;
        }
        
        let suggestions = [];
        
        switch (config.source) {
            case 'users':
                suggestions = await fetchUserSuggestions(query);
                break;
            case 'chats':
                suggestions = await fetchChatSuggestions(query);
                break;
            case 'history':
                suggestions = await fetchHistorySuggestions(query);
                break;
            case 'mixed':
                suggestions = await fetchMixedSuggestions(query);
                break;
            default:
                suggestions = await fetchUserSuggestions(query);
        }
        
        // Cache the results
        autocompleteCache.set(cacheKey, suggestions);
        
        // Limit suggestions
        suggestions = suggestions.slice(0, config.maxSuggestions);
        currentSuggestions = suggestions;
        
        displayAutocompleteSuggestions(suggestions, config);
        
    } catch (error) {
        console.error('Error fetching autocomplete suggestions:', error);
        hideAutocompleteSuggestions();
    }
}

/**
 * Fetch user suggestions
 */
async function fetchUserSuggestions(query) {
    try {
        const response = await fetch(`${CONFIG.API_BASE_URL}/search/users?q=${encodeURIComponent(query)}`);
        const data = await response.json();
        
        if (response.ok && data.users) {
            return data.users.map(user => ({
                type: 'user',
                value: user.username,
                label: user.displayName || user.username,
                subtitle: `@${user.username}`,
                avatar: `/api/user/${encodeURIComponent(user.username)}/avatar`,
                data: user
            }));
        }
        
        return [];
    } catch (error) {
        console.error('Error fetching user suggestions:', error);
        return [];
    }
}

/**
 * Fetch chat suggestions
 */
async function fetchChatSuggestions(query) {
    try {
        const response = await fetch(`${CONFIG.API_BASE_URL}/search/chats?q=${encodeURIComponent(query)}`);
        const data = await response.json();
        
        if (response.ok && data.chats) {
            return data.chats.map(chat => ({
                type: 'chat',
                value: chat.otherUsername,
                label: `Chat with ${chat.otherUsername}`,
                subtitle: chat.lastMessage || 'No messages yet',
                avatar: `/api/user/${encodeURIComponent(chat.otherUsername)}/avatar`,
                data: chat
            }));
        }
        
        return [];
    } catch (error) {
        console.error('Error fetching chat suggestions:', error);
        return [];
    }
}

/**
 * Fetch search history suggestions
 */
async function fetchHistorySuggestions(query) {
    try {
        const response = await fetch(`${CONFIG.API_BASE_URL}/search/suggestions?q=${encodeURIComponent(query)}&type=search`);
        const data = await response.json();
        
        if (response.ok && data.suggestions) {
            return data.suggestions.map(suggestion => ({
                type: 'history',
                value: suggestion,
                label: suggestion,
                subtitle: 'From search history',
                icon: '🔍'
            }));
        }
        
        return [];
    } catch (error) {
        console.error('Error fetching history suggestions:', error);
        return [];
    }
}

/**
 * Fetch mixed suggestions (users + history)
 */
async function fetchMixedSuggestions(query) {
    try {
        const [users, history] = await Promise.all([
            fetchUserSuggestions(query),
            fetchHistorySuggestions(query)
        ]);
        
        // Combine and sort by relevance
        const mixed = [...users.slice(0, 5), ...history.slice(0, 3)];
        return mixed.sort((a, b) => {
            // Prioritize exact matches
            if (a.value.toLowerCase() === query.toLowerCase()) return -1;
            if (b.value.toLowerCase() === query.toLowerCase()) return 1;
            
            // Then by type (users first)
            if (a.type === 'user' && b.type !== 'user') return -1;
            if (b.type === 'user' && a.type !== 'user') return 1;
            
            return 0;
        });
    } catch (error) {
        console.error('Error fetching mixed suggestions:', error);
        return [];
    }
}

/**
 * Display autocomplete suggestions
 */
function displayAutocompleteSuggestions(suggestions, config) {
    if (!currentAutocompleteInput || !suggestions || suggestions.length === 0) {
        hideAutocompleteSuggestions();
        return;
    }
    
    // Get or create suggestions container
    let suggestionsList = document.getElementById('autocompleteSuggestions');
    if (!suggestionsList) {
        suggestionsList = createSuggestionsContainer();
    }
    
    // Generate HTML
    const html = suggestions.map((suggestion, index) => 
        createSuggestionHtml(suggestion, index)
    ).join('');
    
    suggestionsList.innerHTML = html;
    
    // Position and show
    positionSuggestionsList(suggestionsList, currentAutocompleteInput);
    suggestionsList.classList.remove('hidden');
    
    // Add click listeners
    suggestionsList.querySelectorAll('.autocomplete-suggestion').forEach((item, index) => {
        item.addEventListener('click', () => selectSuggestion(item));
        item.addEventListener('mouseenter', () => setActiveSuggestion(
            suggestionsList.querySelectorAll('.autocomplete-suggestion'), index
        ));
    });
}

/**
 * Create suggestions container
 */
function createSuggestionsContainer() {
    const container = document.createElement('div');
    container.id = 'autocompleteSuggestions';
    container.className = 'autocomplete-suggestions hidden';
    document.body.appendChild(container);
    return container;
}

/**
 * Create suggestion HTML
 */
function createSuggestionHtml(suggestion, index) {
    const avatar = suggestion.avatar ? 
        `<img src="${suggestion.avatar}" alt="${escapeHtml(suggestion.label)}" class="suggestion-avatar" onerror="this.src='/images/default-avatar.png'">` :
        `<div class="suggestion-icon">${suggestion.icon || '👤'}</div>`;
    
    return `
        <div class="autocomplete-suggestion ${index === 0 ? 'active' : ''}" data-value="${escapeHtml(suggestion.value)}" data-type="${suggestion.type}">
            ${avatar}
            <div class="suggestion-content">
                <div class="suggestion-label">${escapeHtml(suggestion.label)}</div>
                ${suggestion.subtitle ? `<div class="suggestion-subtitle">${escapeHtml(suggestion.subtitle)}</div>` : ''}
            </div>
            <div class="suggestion-type">${suggestion.type}</div>
        </div>
    `;
}

/**
 * Position suggestions list
 */
function positionSuggestionsList(list, input) {
    const rect = input.getBoundingClientRect();
    const viewportHeight = window.innerHeight;
    
    list.style.left = rect.left + 'px';
    list.style.width = rect.width + 'px';
    list.style.maxWidth = Math.max(rect.width, 300) + 'px';
    
    // Position above or below input based on available space
    const spaceBelow = viewportHeight - rect.bottom;
    const spaceAbove = rect.top;
    
    if (spaceBelow >= 200 || spaceBelow > spaceAbove) {
        list.style.top = rect.bottom + 'px';
        list.style.bottom = 'auto';
    } else {
        list.style.bottom = (viewportHeight - rect.top) + 'px';
        list.style.top = 'auto';
    }
}

/**
 * Set active suggestion
 */
function setActiveSuggestion(suggestions, index) {
    suggestions.forEach((s, i) => {
        s.classList.toggle('active', i === index);
    });
}

/**
 * Select a suggestion
 */
function selectSuggestion(suggestionElement) {
    if (!suggestionElement || !currentAutocompleteInput) return;
    
    const value = suggestionElement.dataset.value;
    const type = suggestionElement.dataset.type;
    
    // Set input value
    currentAutocompleteInput.value = value;
    
    // Call config callback if provided
    const config = currentAutocompleteInput.autocompleteConfig;
    if (config && config.onSelect) {
        const suggestionData = currentSuggestions.find(s => s.value === value);
        config.onSelect(value, type, suggestionData);
    }
    
    // Hide suggestions
    hideAutocompleteSuggestions();
    
    // Trigger change event
    currentAutocompleteInput.dispatchEvent(new Event('change', { bubbles: true }));
}

/**
 * Hide autocomplete suggestions
 */
function hideAutocompleteSuggestions(event) {
    // Delay hiding to allow click events to process
    setTimeout(() => {
        const suggestionsList = document.getElementById('autocompleteSuggestions');
        if (suggestionsList) {
            suggestionsList.classList.add('hidden');
        }
    }, event ? 150 : 0);
}

/**
 * Clear autocomplete cache
 */
function clearAutocompleteCache() {
    autocompleteCache.clear();
    console.log('Autocomplete cache cleared');
}

/**
 * Setup autocomplete for common inputs
 */
function setupCommonAutocompletes() {
    // User search in new chat modal
    const newChatUserSearch = document.getElementById('newChatUserSearch');
    if (newChatUserSearch) {
        initializeAutocomplete(newChatUserSearch, {
            source: 'users',
            onSelect: (value, type, data) => {
                if (data && data.data) {
                    selectUser(data.data.username, data.data.displayName || data.data.username);
                }
            }
        });
    }
    
    // User filter input
    const userFilterInput = document.getElementById('userFilterInput');
    if (userFilterInput) {
        initializeAutocomplete(userFilterInput, {
            source: 'users',
            onSelect: (value, type, data) => {
                addUserFilter(value);
                userFilterInput.value = '';
            }
        });
    }
    
    // Main search input
    const mainSearchInput = document.getElementById('mainSearchInput');
    if (mainSearchInput) {
        initializeAutocomplete(mainSearchInput, {
            source: 'mixed',
            maxSuggestions: 8,
            onSelect: (value, type, data) => {
                if (type === 'user') {
                    startChatFromSearch(value);
                } else {
                    performSearch(value);
                }
            }
        });
    }
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    setTimeout(setupCommonAutocompletes, 1000); // Delay to ensure other elements are loaded
});

// Export autocomplete functions
window.ChatApp = {
    ...window.ChatApp,
    initializeAutocomplete,
    clearAutocompleteCache,
    setupCommonAutocompletes
};

console.log('Autocomplete module loaded successfully');
"""
        },
        
        {
            "path": "src\\main\\resources\\static\\js\\bulk-actions.js",
            "content": r"""// Bulk actions functionality
console.log('Bulk actions module loaded');

// Bulk actions state
let bulkMode = false;
let selectedItems = new Set();
let bulkActionType = null;

/**
 * Initialize bulk actions
 */
function initializeBulkActions() {
    setupBulkActionListeners();
    updateBulkActionButtons();
}

/**
 * Setup bulk action event listeners
 */
function setupBulkActionListeners() {
    // Bulk select toggle button
    const bulkSelectBtn = document.getElementById('bulkSelectBtn');
    if (bulkSelectBtn) {
        bulkSelectBtn.addEventListener('click', toggleBulkMode);
    }
    
    // Select all checkbox
    const selectAllCheckbox = document.getElementById('selectAllCheckbox');
    if (selectAllCheckbox) {
        selectAllCheckbox.addEventListener('change', handleSelectAll);
    }
    
    // Individual item checkboxes (delegated)
    document.addEventListener('change', function(e) {
        if (e.target.classList.contains('chat-select-checkbox') || 
            e.target.classList.contains('message-select-checkbox')) {
            handleItemSelection(e.target);
        }
    });
}

/**
 * Toggle bulk mode
 */
function toggleBulkMode() {
    bulkMode = !bulkMode;
    selectedItems.clear();
    
    const bulkSelectBtn = document.getElementById('bulkSelectBtn');
    const bulkActions = document.getElementById('bulkActions');
    const selectAllContainer = document.getElementById('selectAllContainer');
    
    // Update UI
    if (bulkSelectBtn) {
        bulkSelectBtn.classList.toggle('active', bulkMode);
        bulkSelectBtn.textContent = bulkMode ? 'Cancel' : 'Select';
    }
    
    if (bulkActions) {
        bulkActions.classList.toggle('hidden', !bulkMode);
    }
    
    if (selectAllContainer) {
        selectAllContainer.classList.toggle('hidden', !bulkMode);
    }
    
    // Show/hide checkboxes
    document.body.classList.toggle('bulk-mode', bulkMode);
    
    // Clear all selections when exiting bulk mode
    if (!bulkMode) {
        clearAllSelections();
    }
    
    updateBulkActionButtons();
}

/**
 * Handle select all checkbox
 */
function handleSelectAll(event) {
    const isChecked = event.target.checked;
    const checkboxes = document.querySelectorAll('.chat-select-checkbox, .message-select-checkbox');
    
    checkboxes.forEach(checkbox => {
        checkbox.checked = isChecked;
        handleItemSelection(checkbox);
    });
}

/**
 * Handle individual item selection
 */
function handleItemSelection(checkbox) {
    const itemId = getItemIdFromCheckbox(checkbox);
    const isSelected = checkbox.checked;
    
    if (isSelected) {
        selectedItems.add(itemId);
    } else {
        selectedItems.delete(itemId);
    }
    
    // Update item visual state
    const itemElement = checkbox.closest('.chat-item, .message-bubble');
    if (itemElement) {
        itemElement.classList.toggle('selected', isSelected);
    }
    
    updateBulkActionButtons();
    updateSelectAllCheckbox();
}

/**
 * Get item ID from checkbox
 */
function getItemIdFromCheckbox(checkbox) {
    const itemElement = checkbox.closest('.chat-item, .message-bubble');
    if (itemElement) {
        return itemElement.dataset.chatId || itemElement.dataset.messageId;
    }
    return checkbox.id;
}

/**
 * Update bulk action buttons state
 */
function updateBulkActionButtons() {
    const selectedCount = selectedItems.size;
    const bulkActionButtons = document.querySelectorAll('.bulk-action-btn');
    const selectedCountElement = document.getElementById('selectedCount');
    
    // Update selected count
    if (selectedCountElement) {
        selectedCountElement.textContent = selectedCount;
    }
    
    // Enable/disable bulk action buttons
    bulkActionButtons.forEach(btn => {
        const isCancel = btn.classList.contains('cancel-bulk-btn');
        btn.disabled = !isCancel && selectedCount === 0;
    });
    
    // Update bulk actions visibility
    const bulkActionsContainer = document.getElementById('bulkActions');
    if (bulkActionsContainer) {
        const hasSelection = selectedCount > 0;
        bulkActionsContainer.classList.toggle('has-selection', hasSelection);
    }
}

/**
 * Update select all checkbox state
 */
function updateSelectAllCheckbox() {
    const selectAllCheckbox = document.getElementById('selectAllCheckbox');
    if (!selectAllCheckbox) return;
    
    const allCheckboxes = document.querySelectorAll('.chat-select-checkbox:not(#selectAllCheckbox), .message-select-checkbox');
    const checkedCheckboxes = document.querySelectorAll('.chat-select-checkbox:checked, .message-select-checkbox:checked');
    
    if (allCheckboxes.length === 0) {
        selectAllCheckbox.indeterminate = false;
        selectAllCheckbox.checked = false;
    } else if (checkedCheckboxes.length === allCheckboxes.length) {
        selectAllCheckbox.indeterminate = false;
        selectAllCheckbox.checked = true;
    } else if (checkedCheckboxes.length > 0) {
        selectAllCheckbox.indeterminate = true;
        selectAllCheckbox.checked = false;
    } else {
        selectAllCheckbox.indeterminate = false;
        selectAllCheckbox.checked = false;
    }
}

/**
 * Clear all selections
 */
function clearAllSelections() {
    selectedItems.clear();
    
    // Uncheck all checkboxes
    document.querySelectorAll('.chat-select-checkbox, .message-select-checkbox').forEach(checkbox => {
        checkbox.checked = false;
    });
    
    // Remove selected class from items
    document.querySelectorAll('.chat-item.selected, .message-bubble.selected').forEach(item => {
        item.classList.remove('selected');
    });
    
    updateBulkActionButtons();
    updateSelectAllCheckbox();
}

/**
 * Get selected item IDs
 */
function getSelectedItemIds() {
    return Array.from(selectedItems);
}

/**
 * Perform bulk delete action
 */
async function performBulkDelete() {
    const selectedIds = getSelectedItemIds();
    
    if (selectedIds.length === 0) {
        showNotification('No items selected', 'warning');
        return;
    }
    
    const confirmMessage = `Delete ${selectedIds.length} item(s)? This action cannot be undone.`;
    if (!confirm(confirmMessage)) {
        return;
    }
    
    try {
        const response = await fetch(`${CONFIG.API_BASE_URL}/chat/bulk-action`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                actionType: 'DELETE_CHATS',
                chatIds: selectedIds.map(id => parseInt(id))
            })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            showNotification(`Deleted ${data.processedCount} item(s)`, 'success');
            
            // Remove deleted items from UI
            selectedIds.forEach(id => {
                const item = document.querySelector(`[data-chat-id="${id}"], [data-message-id="${id}"]`);
                if (item) {
                    item.remove();
                }
            });
            
            // Exit bulk mode
            toggleBulkMode();
            
            // Refresh data
            if (typeof loadUserChats === 'function') {
                loadUserChats();
            }
            
        } else {
            throw new Error(data.error || 'Failed to delete items');
        }
        
    } catch (error) {
        console.error('Error performing bulk delete:', error);
        showNotification('Failed to delete items', 'error');
    }
}

/**
 * Perform bulk pin action
 */
async function performBulkPin() {
    const selectedIds = getSelectedItemIds();
    
    if (selectedIds.length === 0) {
        showNotification('No chats selected', 'warning');
        return;
    }
    
    try {
        const response = await fetch(`${CONFIG.API_BASE_URL}/chat/bulk-action`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                actionType: 'PIN_CHATS',
                chatIds: selectedIds.map(id => parseInt(id))
            })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            showNotification(`Pinned ${data.processedCount} chat(s)`, 'success');
            
            // Update UI
            selectedIds.forEach(id => {
                const chatItem = document.querySelector(`[data-chat-id="${id}"]`);
                if (chatItem) {
                    const indicators = chatItem.querySelector('.chat-indicators');
                    if (indicators && !indicators.querySelector('.pinned-indicator')) {
                        indicators.insertAdjacentHTML('afterbegin', '<span class="pinned-indicator">📌</span>');
                    }
                }
            });
            
            // Exit bulk mode
            toggleBulkMode();
            
            // Refresh data
            if (typeof loadUserChats === 'function') {
                loadUserChats();
            }
            
        } else {
            throw new Error(data.error || 'Failed to pin chats');
        }
        
    } catch (error) {
        console.error('Error performing bulk pin:', error);
        showNotification('Failed to pin chats', 'error');
    }
}

/**
 * Perform bulk unpin action
 */
async function performBulkUnpin() {
    const selectedIds = getSelectedItemIds();
    
    if (selectedIds.length === 0) {
        showNotification('No chats selected', 'warning');
        return;
    }
    
    try {
        const response = await fetch(`${CONFIG.API_BASE_URL}/chat/bulk-action`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                actionType: 'UNPIN_CHATS',
                chatIds: selectedIds.map(id => parseInt(id))
            })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            showNotification(`Unpinned ${data.processedCount} chat(s)`, 'success');
            
            // Update UI
            selectedIds.forEach(id => {
                const chatItem = document.querySelector(`[data-chat-id="${id}"]`);
                if (chatItem) {
                    const pinnedIndicator = chatItem.querySelector('.pinned-indicator');
                    if (pinnedIndicator) {
                        pinnedIndicator.remove();
                    }
                }
            });
            
            // Exit bulk mode
            toggleBulkMode();
            
            // Refresh data
            if (typeof loadUserChats === 'function') {
                loadUserChats();
            }
            
        } else {
            throw new Error(data.error || 'Failed to unpin chats');
        }
        
    } catch (error) {
        console.error('Error performing bulk unpin:', error);
        showNotification('Failed to unpin chats', 'error');
    }
}

/**
 * Perform bulk archive action
 */
async function performBulkArchive() {
    const selectedIds = getSelectedItemIds();
    
    if (selectedIds.length === 0) {
        showNotification('No chats selected', 'warning');
        return;
    }
    
    try {
        const response = await fetch(`${CONFIG.API_BASE_URL}/chat/bulk-action`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                actionType: 'ARCHIVE_CHATS',
                chatIds: selectedIds.map(id => parseInt(id))
            })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            showNotification(`Archived ${data.processedCount} chat(s)`, 'success');
            
            // Remove archived chats from current view (if not showing archived)
            const showArchived = document.querySelector('[data-filter="archived"]')?.classList.contains('active');
            if (!showArchived) {
                selectedIds.forEach(id => {
                    const chatItem = document.querySelector(`[data-chat-id="${id}"]`);
                    if (chatItem) {
                        chatItem.remove();
                    }
                });
            }
            
            // Exit bulk mode
            toggleBulkMode();
            
            // Refresh data
            if (typeof loadUserChats === 'function') {
                loadUserChats();
            }
            
        } else {
            throw new Error(data.error || 'Failed to archive chats');
        }
        
    } catch (error) {
        console.error('Error performing bulk archive:', error);
        showNotification('Failed to archive chats', 'error');
    }
}

/**
 * Perform bulk block action
 */
async function performBulkBlock() {
    const selectedIds = getSelectedItemIds();
    
    if (selectedIds.length === 0) {
        showNotification('No chats selected', 'warning');
        return;
    }
    
    // Get usernames from selected chats
    const usernames = selectedIds.map(id => {
        const chatItem = document.querySelector(`[data-chat-id="${id}"]`);
        return chatItem?.querySelector('.chat-username')?.textContent;
    }).filter(Boolean);
    
    if (usernames.length === 0) {
        showNotification('No valid users to block', 'error');
        return;
    }
    
    const confirmMessage = `Block ${usernames.length} user(s)? You won't receive messages from them.`;
    if (!confirm(confirmMessage)) {
        return;
    }
    
    try {
        const response = await fetch(`${CONFIG.API_BASE_URL}/block/bulk-block`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                usernames: usernames,
                reason: 'Bulk block action'
            })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            showNotification(`Blocked ${data.blockedCount} user(s)`, 'success');
            
            // Remove blocked chats from UI
            selectedIds.forEach(id => {
                const chatItem = document.querySelector(`[data-chat-id="${id}"]`);
                if (chatItem) {
                    chatItem.remove();
                }
            });
            
            // Exit bulk mode
            toggleBulkMode();
            
            // Refresh data
            if (typeof loadUserChats === 'function') {
                loadUserChats();
            }
            
        } else {
            throw new Error(data.error || 'Failed to block users');
        }
        
    } catch (error) {
        console.error('Error performing bulk block:', error);
        showNotification('Failed to block users', 'error');
    }
}

/**
 * Show bulk action confirmation modal
 */
function showBulkActionConfirmation(actionType) {
    const selectedCount = selectedItems.size;
    if (selectedCount === 0) {
        showNotification('No items selected', 'warning');
        return;
    }
    
    let actionText = '';
    let warningText = '';
    
    switch (actionType) {
        case 'delete':
            actionText = 'Delete';
            warningText = 'This action cannot be undone.';
            break;
        case 'block':
            actionText = 'Block';
            warningText = 'You will no longer receive messages from these users.';
            break;
        case 'archive':
            actionText = 'Archive';
            warningText = 'These chats will be moved to archived.';
            break;
    }
    
    const modalHtml = `
        <div class="modal-overlay">
            <div class="modal modal-medium">
                <div class="modal-header">
                    <h3 class="modal-title">Confirm Bulk ${actionText}</h3>
                    <button class="modal-close" onclick="closeModal()">&times;</button>
                </div>
                <div class="modal-body">
                    <p>${actionText} ${selectedCount} selected item(s)?</p>
                    <p class="warning-text">${warningText}</p>
                </div>
                <div class="modal-footer">
                    <button onclick="closeModal()" class="btn btn-secondary">Cancel</button>
                    <button onclick="confirmBulkAction('${actionType}')" class="btn btn-danger">${actionText}</button>
                </div>
            </div>
        </div>
    `;
    
    document.body.insertAdjacentHTML('beforeend', modalHtml);
    setTimeout(() => document.querySelector('.modal-overlay').classList.add('show'), 10);
}

/**
 * Confirm bulk action
 */
function confirmBulkAction(actionType) {
    closeModal();
    
    switch (actionType) {
        case 'delete':
            performBulkDelete();
            break;
        case 'pin':
            performBulkPin();
            break;
        case 'unpin':
            performBulkUnpin();
            break;
        case 'archive':
            performBulkArchive();
            break;
        case 'block':
            performBulkBlock();
            break;
    }
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', initializeBulkActions);

// Export bulk actions functions
window.ChatApp = {
    ...window.ChatApp,
    toggleBulkMode,
    performBulkDelete,
    performBulkPin,
    performBulkUnpin,
    performBulkArchive,
    performBulkBlock,
    clearAllSelections,
    getSelectedItemIds
};

console.log('Bulk actions module loaded successfully');
"""
        },
        
        {
            "path": "src\\main\\resources\\static\\js\\export.js",
            "content": r"""// Export functionality
console.log('Export module loaded');

// Export state
let currentExportId = null;
let exportStatusInterval = null;

/**
 * Show export modal
 */
function showExportModal() {
    const modalHtml = `
        <div class="modal-overlay">
            <div class="modal modal-large">
                <div class="modal-header">
                    <h3 class="modal-title">Export Chats</h3>
                    <button class="modal-close" onclick="closeModal()">&times;</button>
                </div>
                <div class="modal-body export-modal">
                    <div class="export-options">
                        <div class="export-option" data-format="TXT" onclick="selectExportFormat('TXT')">
                            <h5>📄 Text File</h5>
                            <p>Plain text format, easy to read</p>
                        </div>
                        <div class="export-option" data-format="JSON" onclick="selectExportFormat('JSON')">
                            <h5>📋 JSON File</h5>
                            <p>Structured data with metadata</p>
                        </div>
                        <div class="export-option" data-format="CSV" onclick="selectExportFormat('CSV')">
                            <h5>📊 CSV File</h5>
                            <p>Spreadsheet compatible format</p>
                        </div>
                    </div>
                    
                    <div class="export-settings">
                        <h4>Export Settings</h4>
                        
                        <div class="setting-group">
                            <label>Chat Selection:</label>
                            <div class="radio-group">
                                <label class="radio-label">
                                    <input type="radio" name="chatSelection" value="all" checked>
                                    <span class="radio-checkmark"></span>
                                    All Chats
                                </label>
                                <label class="radio-label">
                                    <input type="radio" name="chatSelection" value="selected">
                                    <span class="radio-checkmark"></span>
                                    Selected Chats Only
                                </label>
                                <label class="radio-label">
                                    <input type="radio" name="chatSelection" value="pinned">
                                    <span class="radio-checkmark"></span>
                                    Pinned Chats Only
                                </label>
                            </div>
                        </div>
                        
                        <div class="setting-group">
                            <label>Date Range:</label>
                            <div class="date-range">
                                <input type="date" id="exportDateFrom" placeholder="From">
                                <input type="date" id="exportDateTo" placeholder="To">
                            </div>
                            <div class="quick-dates">
                                <button onclick="setExportDateRange('week')" class="btn btn-small">Last Week</button>
                                <button onclick="setExportDateRange('month')" class="btn btn-small">Last Month</button>
                                <button onclick="setExportDateRange('all')" class="btn btn-small">All Time</button>
                            </div>
                        </div>
                        
                        <div class="setting-group">
                            <label>Options:</label>
                            <div class="checkbox-group">
                                <label class="checkbox-label">
                                    <input type="checkbox" id="includeImages" checked>
                                    <span class="checkmark"></span>
                                    Include Images
                                </label>
                                <label class="checkbox-label">
                                    <input type="checkbox" id="includeMetadata" checked>
                                    <span class="checkmark"></span>
                                    Include Metadata
                                </label>
                                <label class="checkbox-label">
                                    <input type="checkbox" id="includeSystemMessages">
                                    <span class="checkmark"></span>
                                    Include System Messages
                                </label>
                            </div>
                        </div>
                        
                        <div class="setting-group">
                            <label for="maxMessages">Maximum Messages:</label>
                            <input type="number" id="maxMessages" value="1000" min="1" max="10000">
                            <small>Leave empty for no limit</small>
                        </div>
                    </div>
                </div>
                <div class="modal-footer">
                    <button onclick="closeModal()" class="btn btn-secondary">Cancel</button>
                    <button onclick="startExport()" class="btn btn-primary" id="startExportBtn" disabled>Start Export</button>
                </div>
            </div>
        </div>
    `;
    
    document.body.insertAdjacentHTML('beforeend', modalHtml);
    setTimeout(() => document.querySelector('.modal-overlay').classList.add('show'), 10);
}

/**
 * Select export format
 */
function selectExportFormat(format) {
    // Remove previous selection
    document.querySelectorAll('.export-option').forEach(option => {
        option.classList.remove('selected');
    });
    
    // Select new format
    const selectedOption = document.querySelector(`[data-format="${format}"]`);
    if (selectedOption) {
        selectedOption.classList.add('selected');
    }
    
    // Enable start button
    const startBtn = document.getElementById('startExportBtn');
    if (startBtn) {
        startBtn.disabled = false;
    }
}

/**
 * Set export date range
 */
function setExportDateRange(range) {
    const fromInput = document.getElementById('exportDateFrom');
    const toInput = document.getElementById('exportDateTo');
    
    if (!fromInput || !toInput) return;
    
    const now = new Date();
    const today = now.toISOString().split('T')[0];
    
    toInput.value = today;
    
    switch (range) {
        case 'week':
            const weekAgo = new Date(now.getTime() - 7 * 24 * 60 * 60 * 1000);
            fromInput.value = weekAgo.toISOString().split('T')[0];
            break;
        case 'month':
            const monthAgo = new Date(now.getFullYear(), now.getMonth() - 1, now.getDate());
            fromInput.value = monthAgo.toISOString().split('T')[0];
            break;
        case 'all':
            fromInput.value = '';
            toInput.value = '';
            break;
    }
}

/**
 * Start export process
 */
async function startExport() {
    const selectedFormat = document.querySelector('.export-option.selected');
    if (!selectedFormat) {
        showNotification('Please select an export format', 'warning');
        return;
    }
    
    const exportFormat = selectedFormat.dataset.format;
    const exportData = getExportData();
    
    try {
        const response = await fetch(`${CONFIG.API_BASE_URL}/export/chats`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                exportFormat: exportFormat,
                ...exportData
            })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            currentExportId = data.export.exportId;
            closeModal();
            showExportProgress(data.export);
            startExportStatusPolling();
        } else {
            throw new Error(data.error || 'Failed to start export');
        }
        
    } catch (error) {
        console.error('Error starting export:', error);
        showNotification('Failed to start export', 'error');
    }
}

/**
 * Get export data from form
 */
function getExportData() {
    const chatSelection = document.querySelector('input[name="chatSelection"]:checked')?.value || 'all';
    const dateFrom = document.getElementById('exportDateFrom')?.value;
    const dateTo = document.getElementById('exportDateTo')?.value;
    const includeImages = document.getElementById('includeImages')?.checked || false;
    const includeMetadata = document.getElementById('includeMetadata')?.checked || false;
    const includeSystemMessages = document.getElementById('includeSystemMessages')?.checked || false;
    const maxMessages = document.getElementById('maxMessages')?.value;
    
    const exportData = {
        chatSelection: chatSelection,
        includeImages: includeImages,
        includeMetadata: includeMetadata,
        includeSystemMessages: includeSystemMessages
    };
    
    if (dateFrom) exportData.dateFrom = new Date(dateFrom).toISOString();
    if (dateTo) exportData.dateTo = new Date(dateTo).toISOString();
    if (maxMessages) exportData.maxMessages = parseInt(maxMessages);
    
    // Get chat IDs based on selection
    if (chatSelection === 'selected') {
        exportData.chatIds = getSelectedItemIds();
    } else if (chatSelection === 'pinned') {
        const pinnedChats = document.querySelectorAll('.chat-item .pinned-indicator');
        exportData.chatIds = Array.from(pinnedChats).map(indicator => {
            const chatItem = indicator.closest('.chat-item');
            return parseInt(chatItem.dataset.chatId);
        });
    }
    
    return exportData;
}

/**
 * Show export progress modal
 */
function showExportProgress(exportInfo) {
    const modalHtml = `
        <div class="modal-overlay">
            <div class="modal modal-medium">
                <div class="modal-header">
                    <h3 class="modal-title">Exporting Chats</h3>
                </div>
                <div class="modal-body progress-modal">
                    <div class="export-info">
                        <p>Format: <strong>${exportInfo.exportFormat}</strong></p>
                        <p>Started: <strong>${formatDate(exportInfo.createdAt)}</strong></p>
                    </div>
                    
                    <div class="progress-container">
                        <div class="progress-bar">
                            <div class="progress-fill" id="exportProgressFill" style="width: 0%"></div>
                        </div>
                        <div class="progress-text" id="exportProgressText">Preparing export...</div>
                    </div>
                    
                    <div class="export-status" id="exportStatus">
                        <p>Status: <span id="exportStatusText">In Progress</span></p>
                        <p id="exportDetails"></p>
                    </div>
                </div>
                <div class="modal-footer">
                    <button onclick="cancelExport()" class="btn btn-secondary">Cancel</button>
                    <button onclick="closeModal()" class="btn btn-primary" id="closeProgressBtn" disabled>Close</button>
                </div>
            </div>
        </div>
    `;
    
    document.body.insertAdjacentHTML('beforeend', modalHtml);
    setTimeout(() => document.querySelector('.modal-overlay').classList.add('show'), 10);
}

/**
 * Start export status polling
 */
function startExportStatusPolling() {
    exportStatusInterval = setInterval(async () => {
        try {
            const response = await fetch(`${CONFIG.API_BASE_URL}/export/status/${currentExportId}`);
            const data = await response.json();
            
            if (response.ok) {
                updateExportProgress(data);
                
                if (data.exportStatus === 'COMPLETED') {
                    stopExportStatusPolling();
                    showExportComplete(data);
                } else if (data.exportStatus === 'FAILED') {
                    stopExportStatusPolling();
                    showExportError(data.errorMessage);
                }
            }
        } catch (error) {
            console.error('Error checking export status:', error);
        }
    }, 2000); // Poll every 2 seconds
}

/**
 * Stop export status polling
 */
function stopExportStatusPolling() {
    if (exportStatusInterval) {
        clearInterval(exportStatusInterval);
        exportStatusInterval = null;
    }
}

/**
 * Update export progress
 */
function updateExportProgress(exportData) {
    const progressFill = document.getElementById('exportProgressFill');
    const progressText = document.getElementById('exportProgressText');
    const statusText = document.getElementById('exportStatusText');
    const details = document.getElementById('exportDetails');
    
    if (progressFill && exportData.progress) {
        progressFill.style.width = exportData.progress + '%';
    }
    
    if (progressText) {
        progressText.textContent = exportData.statusMessage || 'Processing...';
    }
    
    if (statusText) {
        statusText.textContent = exportData.exportStatus || 'In Progress';
    }
    
    if (details && exportData.messageCount) {
        details.innerHTML = `Messages processed: <strong>${exportData.messageCount}</strong>`;
    }
}

/**
 * Show export complete
 */
function showExportComplete(exportData) {
    const progressText = document.getElementById('exportProgressText');
    const statusText = document.getElementById('exportStatusText');
    const closeBtn = document.getElementById('closeProgressBtn');
    const details = document.getElementById('exportDetails');
    
    if (progressText) {
        progressText.textContent = 'Export completed successfully!';
    }
    
    if (statusText) {
        statusText.textContent = 'Completed';
        statusText.style.color = 'var(--success-color)';
    }
    
    if (closeBtn) {
        closeBtn.disabled = false;
        closeBtn.textContent = 'Download';
        closeBtn.onclick = () => downloadExportFile(exportData.downloadUrl);
    }
    
    if (details) {
        details.innerHTML = `
            <p>Total messages: <strong>${exportData.messageCount}</strong></p>
            <p>File size: <strong>${formatFileSize(exportData.fileSize)}</strong></p>
            <p>Format: <strong>${exportData.exportFormat}</strong></p>
        `;
    }
    
    showNotification('Export completed successfully!', 'success');
}

/**
 * Show export error
 */
function showExportError(errorMessage) {
    const progressText = document.getElementById('exportProgressText');
    const statusText = document.getElementById('exportStatusText');
    const closeBtn = document.getElementById('closeProgressBtn');
    
    if (progressText) {
        progressText.textContent = 'Export failed';
    }
    
    if (statusText) {
        statusText.textContent = 'Failed';
        statusText.style.color = 'var(--danger-color)';
    }
    
    if (closeBtn) {
        closeBtn.disabled = false;
        closeBtn.textContent = 'Close';
    }
    
    showNotification(`Export failed: ${errorMessage}`, 'error');
}

/**
 * Cancel export
 */
async function cancelExport() {
    if (!currentExportId) return;
    
    try {
        const response = await fetch(`${CONFIG.API_BASE_URL}/export/cancel/${currentExportId}`, {
            method: 'POST'
        });
        
        if (response.ok) {
            stopExportStatusPolling();
            closeModal();
            showNotification('Export cancelled', 'info');
        }
    } catch (error) {
        console.error('Error cancelling export:', error);
    }
}

/**
 * Download export file
 */
function downloadExportFile(downloadUrl) {
    if (!downloadUrl) {
        showNotification('Download URL not available', 'error');
        return;
    }
    
    const link = document.createElement('a');
    link.href = downloadUrl;
    link.download = '';
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    
    closeModal();
    showNotification('Download started', 'success');
}

/**
 * Quick export current chat
 */
async function quickExportCurrentChat(format = 'TXT') {
    if (!activeChat) {
        showNotification('No active chat to export', 'warning');
        return;
    }
    
    try {
        const response = await fetch(`${CONFIG.API_BASE_URL}/export/chat/${activeChat.id}?format=${format}`);
        
        if (response.ok) {
            const blob = await response.blob();
            const url = URL.createObjectURL(blob);
            
            const link = document.createElement('a');
            link.href = url;
            link.download = `chat-${activeChat.otherUsername}-${new Date().toISOString().split('T')[0]}.${format.toLowerCase()}`;
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
            
            URL.revokeObjectURL(url);
            showNotification('Chat exported successfully', 'success');
        } else {
            throw new Error('Failed to export chat');
        }
    } catch (error) {
        console.error('Error exporting chat:', error);
        showNotification('Failed to export chat', 'error');
    }
}

// Export functions
window.ChatApp = {
    ...window.ChatApp,
    showExportModal,
    quickExportCurrentChat
};

console.log('Export module loaded successfully');
"""
        },
        
        {
            "path": "src\\main\\resources\\static\\js\\image-handler.js",
            "content": r"""// Image handling functionality
console.log('Image handler module loaded');

// Image handler state
let imageViewerOpen = false;
let currentImageIndex = 0;
let currentImageList = [];

/**
 * Initialize image handling
 */
function initializeImageHandler() {
    setupImageUploadHandler();
    setupImageViewerKeyboardEvents();
    setupImageLazyLoading();
}

/**
 * Setup image upload handler
 */
function setupImageUploadHandler() {
    // File input for image upload
    const imageInput = document.getElementById('imageInput');
    if (imageInput) {
        imageInput.addEventListener('change', handleImageUpload);
    }
    
    // Drag and drop for image upload
    const messageInput = document.getElementById('messageInput');
    if (messageInput) {
        messageInput.addEventListener('dragover', handleDragOver);
        messageInput.addEventListener('drop', handleImageDrop);
    }
    
    // Paste event for images
    document.addEventListener('paste', handleImagePaste);
}

/**
 * Handle image upload
 */
async function handleImageUpload(event) {
    const files = event.target.files;
    if (!files || files.length === 0) return;
    
    for (const file of files) {
        if (file.type.startsWith('image/')) {
            await uploadAndSendImage(file);
        } else {
            showNotification('Please select image files only', 'warning');
        }
    }
    
    // Clear input
    event.target.value = '';
}

/**
 * Handle drag over
 */
function handleDragOver(event) {
    event.preventDefault();
    event.currentTarget.classList.add('drag-over');
}

/**
 * Handle image drop
 */
function handleImageDrop(event) {
    event.preventDefault();
    event.currentTarget.classList.remove('drag-over');
    
    const files = event.dataTransfer.files;
    if (!files || files.length === 0) return;
    
    for (const file of files) {
        if (file.type.startsWith('image/')) {
            uploadAndSendImage(file);
        } else {
            showNotification('Please drop image files only', 'warning');
        }
    }
}

/**
 * Handle image paste
 */
function handleImagePaste(event) {
    const items = event.clipboardData?.items;
    if (!items) return;
    
    for (const item of items) {
        if (item.type.startsWith('image/')) {
            const file = item.getAsFile();
            if (file) {
                uploadAndSendImage(file);
            }
        }
    }
}

/**
 * Upload and send image
 */
async function uploadAndSendImage(file) {
    if (!activeChat) {
        showNotification('Please select a chat first', 'warning');
        return;
    }
    
    // Validate file size (max 10MB)
    const maxSize = 10 * 1024 * 1024;
    if (file.size > maxSize) {
        showNotification('Image is too large. Maximum size is 10MB', 'error');
        return;
    }
    
    try {
        // Show upload progress
        const messageId = 'temp_' + Date.now();
        showImageUploadProgress(messageId, file);
        
        // Create form data
        const formData = new FormData();
        formData.append('image', file);
        formData.append('chatId', activeChat.id);
        
        // Upload image
        const response = await fetch(`${CONFIG.API_BASE_URL}/upload/image`, {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        
        if (response.ok) {
            // Remove progress indicator
            removeImageUploadProgress(messageId);
            
            // Send image message
            const messageData = {
                messageContent: '',
                messageType: 'IMAGE',
                imageUrl: data.imageUrl
            };
            
            const messageResponse = await fetch(`${CONFIG.API_BASE_URL}/chat/${activeChat.id}/send`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(messageData)
            });
            
            const messageResult = await messageResponse.json();
            
            if (messageResponse.ok) {
                addMessageToUI(messageResult.message);
                showNotification('Image sent successfully', 'success', 1500);
            } else {
                throw new Error(messageResult.error || 'Failed to send image message');
            }
            
        } else {
            throw new Error(data.error || 'Failed to upload image');
        }
        
    } catch (error) {
        console.error('Error uploading image:', error);
        removeImageUploadProgress(messageId);
        showNotification('Failed to upload image', 'error');
    }
}

/**
 * Show image upload progress
 */
function showImageUploadProgress(messageId, file) {
    if (!messageContainer) return;
    
    const progressHtml = `
        <div class="message-bubble own-message upload-progress" data-temp-id="${messageId}">
            <div class="message-content">
                <div class="image-upload-progress">
                    <div class="upload-preview">
                        <img src="${URL.createObjectURL(file)}" alt="Uploading..." class="upload-preview-img">
                        <div class="upload-overlay">
                            <div class="upload-spinner"></div>
                            <span>Uploading...</span>
                        </div>
                    </div>
                    <div class="upload-info">
                        <span class="file-name">${file.name}</span>
                        <span class="file-size">${formatFileSize(file.size)}</span>
                    </div>
                </div>
            </div>
        </div>
    `;
    
    messageContainer.insertAdjacentHTML('beforeend', progressHtml);
    
    if (shouldAutoScroll) {
        setTimeout(scrollToBottom, 100);
    }
}

/**
 * Remove image upload progress
 */
function removeImageUploadProgress(messageId) {
    const progressElement = document.querySelector(`[data-temp-id="${messageId}"]`);
    if (progressElement) {
        progressElement.remove();
    }
}

/**
 * Open image viewer
 */
function openImageViewer(imageUrl, chatId = null) {
    // Collect all images in current chat
    if (chatId && chatId === activeChat?.id) {
        currentImageList = Array.from(document.querySelectorAll('.message-image')).map(img => img.src);
        currentImageIndex = currentImageList.indexOf(imageUrl);
    } else {
        currentImageList = [imageUrl];
        currentImageIndex = 0;
    }
    
    const modalHtml = `
        <div class="modal-overlay image-viewer">
            <div class="image-viewer-modal">
                <div class="image-viewer-content">
                    <img id="viewerImage" src="${imageUrl}" alt="Image">
                    <div class="image-viewer-controls">
                        ${currentImageList.length > 1 ? `
                            <button onclick="previousImage()" class="viewer-btn" title="Previous">⬅️</button>
                            <button onclick="nextImage()" class="viewer-btn" title="Next">➡️</button>
                        ` : ''}
                        <button onclick="downloadImage('${imageUrl}')" class="viewer-btn" title="Download">⬇️</button>
                        <button onclick="closeImageViewer()" class="viewer-btn" title="Close">✖️</button>
                    </div>
                    ${currentImageList.length > 1 ? `
                        <div class="image-counter">
                            <span id="imageCounter">${currentImageIndex + 1} of ${currentImageList.length}</span>
                        </div>
                    ` : ''}
                </div>
            </div>
        </div>
    `;
    
    document.body.insertAdjacentHTML('beforeend', modalHtml);
    setTimeout(() => {
        document.querySelector('.image-viewer').classList.add('show');
        imageViewerOpen = true;
    }, 10);
}

/**
 * Close image viewer
 */
function closeImageViewer() {
    const viewer = document.querySelector('.image-viewer');
    if (viewer) {
        viewer.classList.remove('show');
        setTimeout(() => viewer.remove(), 300);
    }
    imageViewerOpen = false;
}

/**
 * Show next image
 */
function nextImage() {
    if (currentImageIndex < currentImageList.length - 1) {
        currentImageIndex++;
        updateViewerImage();
    }
}

/**
 * Show previous image
 */
function previousImage() {
    if (currentImageIndex > 0) {
        currentImageIndex--;
        updateViewerImage();
    }
}

/**
 * Update viewer image
 */
function updateViewerImage() {
    const viewerImage = document.getElementById('viewerImage');
    const counter = document.getElementById('imageCounter');
    
    if (viewerImage && currentImageList[currentImageIndex]) {
        viewerImage.src = currentImageList[currentImageIndex];
    }
    
    if (counter) {
        counter.textContent = `${currentImageIndex + 1} of ${currentImageList.length}`;
    }
}

/**
 * Setup image viewer keyboard events
 */
function setupImageViewerKeyboardEvents() {
    document.addEventListener('keydown', function(event) {
        if (!imageViewerOpen) return;
        
        switch (event.key) {
            case 'ArrowLeft':
                event.preventDefault();
                previousImage();
                break;
            case 'ArrowRight':
                event.preventDefault();
                nextImage();
                break;
            case 'Escape':
                event.preventDefault();
                closeImageViewer();
                break;
        }
    });
}

/**
 * Download image
 */
function downloadImage(imageUrl) {
    const link = document.createElement('a');
    link.href = imageUrl;
    link.download = 'image-' + Date.now() + '.jpg';
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    
    showNotification('Image download started', 'success', 1500);
}

/**
 * Show/hide image in message
 */
function toggleImageVisibility(imageElement) {
    const messageContent = imageElement.closest('.message-content');
    if (!messageContent) return;
    
    const isHidden = imageElement.style.display === 'none';
    
    if (isHidden) {
        showImageInMessage(imageElement);
    } else {
        hideImageInMessage(imageElement);
    }
}

/**
 * Show image in message
 */
function showImageInMessage(imageElement) {
    imageElement.style.display = 'block';
    
    // Update hide/show button
    const messageContainer = imageElement.closest('.image-message');
    if (messageContainer) {
        let hideBtn = messageContainer.querySelector('.hide-image-btn');
        if (!hideBtn) {
            hideBtn = document.createElement('button');
            hideBtn.className = 'hide-image-btn';
            hideBtn.textContent = 'Hide';
            hideBtn.onclick = () => hideImageInMessage(imageElement);
            messageContainer.appendChild(hideBtn);
        }
        
        // Remove show button
        const showBtn = messageContainer.querySelector('.show-image-btn');
        if (showBtn) {
            showBtn.remove();
        }
    }
}

/**
 * Hide image in message
 */
function hideImageInMessage(imageElement) {
    imageElement.style.display = 'none';
    
    // Update hide/show button
    const messageContainer = imageElement.closest('.image-message');
    if (messageContainer) {
        let showBtn = messageContainer.querySelector('.show-image-btn');
        if (!showBtn) {
            showBtn = document.createElement('button');
            showBtn.className = 'show-image-btn';
            showBtn.textContent = 'Show Image';
            showBtn.onclick = () => showImageInMessage(imageElement);
            messageContainer.appendChild(showBtn);
        }
        
        // Remove hide button
        const hideBtn = messageContainer.querySelector('.hide-image-btn');
        if (hideBtn) {
            hideBtn.remove();
        }
    }
}

/**
 * Setup lazy loading for images
 */
function setupImageLazyLoading() {
    if ('IntersectionObserver' in window) {
        const imageObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    if (img.dataset.src) {
                        img.src = img.dataset.src;
                        img.removeAttribute('data-src');
                        observer.unobserve(img);
                    }
                }
            });
        });
        
        // Observe all images with data-src attribute
        document.querySelectorAll('img[data-src]').forEach(img => {
            imageObserver.observe(img);
        });
    }
}

/**
 * Compress image before upload
 */
function compressImage(file, maxWidth = 1920, maxHeight = 1080, quality = 0.8) {
    return new Promise((resolve) => {
        const canvas = document.createElement('canvas');
        const ctx = canvas.getContext('2d');
        const img = new Image();
        
        img.onload = function() {
            // Calculate new dimensions
            let { width, height } = img;
            
            if (width > maxWidth || height > maxHeight) {
                const ratio = Math.min(maxWidth / width, maxHeight / height);
                width *= ratio;
                height *= ratio;
            }
            
            // Set canvas dimensions
            canvas.width = width;
            canvas.height = height;
            
            // Draw and compress
            ctx.drawImage(img, 0, 0, width, height);
            
            canvas.toBlob((blob) => {
                resolve(blob);
            }, 'image/jpeg', quality);
        };
        
        img.src = URL.createObjectURL(file);
    });
}

/**
 * Validate image file
 */
function validateImageFile(file) {
    const allowedTypes = ['image/jpeg', 'image/jpg', 'image/png', 'image/gif', 'image/webp'];
    const maxSize = 10 * 1024 * 1024; // 10MB
    
    if (!allowedTypes.includes(file.type)) {
        throw new Error('Unsupported image format. Please use JPEG, PNG, GIF, or WebP.');
    }
    
    if (file.size > maxSize) {
        throw new Error('Image is too large. Maximum size is 10MB.');
    }
    
    return true;
}

/**
 * Create image thumbnail
 */
function createImageThumbnail(file, size = 150) {
    return new Promise((resolve) => {
        const canvas = document.createElement('canvas');
        const ctx = canvas.getContext('2d');
        const img = new Image();
        
        img.onload = function() {
            canvas.width = size;
            canvas.height = size;
            
            // Calculate crop area for square thumbnail
            const minDimension = Math.min(img.width, img.height);
            const cropX = (img.width - minDimension) / 2;
            const cropY = (img.height - minDimension) / 2;
            
            ctx.drawImage(img, cropX, cropY, minDimension, minDimension, 0, 0, size, size);
            
            canvas.toBlob((blob) => {
                resolve(URL.createObjectURL(blob));
            }, 'image/jpeg', 0.8);
        };
        
        img.src = URL.createObjectURL(file);
    });
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', initializeImageHandler);

// Export image handler functions
window.ChatApp = {
    ...window.ChatApp,
    openImageViewer,
    closeImageViewer,
    downloadImage,
    toggleImageVisibility,
    compressImage,
    validateImageFile
};

console.log('Image handler module loaded successfully');
"""
        }
    ]
    
    # Function to create files
    def create_files(files_list):
        print("\nCreating remaining JavaScript files...")
        
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
    
    # Create all remaining JS files
    create_files(remaining_js_files)
    
    print("\n" + "="*70)
    print("Remaining JavaScript files created successfully!")
    print("="*70)
    
    print("\nCreated Remaining JavaScript Files:")
    print("✓ search.js - Advanced search with filters and history")
    print("✓ filters.js - Data filtering and sorting functionality") 
    print("✓ autocomplete.js - Smart autocomplete for inputs")
    print("✓ bulk-actions.js - Bulk operations on chats/messages")
    print("✓ export.js - Export chats to various formats")
    print("✓ image-handler.js - Image upload, viewing, and processing")
    
    print("\nAdvanced Features Added:")
    print("• 🔍 Advanced search with autocomplete and suggestions")
    print("• 🎛️ Comprehensive filtering with date ranges and presets")
    print("• 💡 Smart autocomplete for users, chats, and search history")
    print("• ⚡ Bulk operations (delete, pin, archive, block)")
    print("• 📤 Export chats to TXT, JSON, and CSV formats")
    print("• 🖼️ Full image handling with viewer, upload, and compression")
    print("• 📱 Drag & drop and paste support for images")
    print("• 🚀 Lazy loading and image optimization")
    
    print("\nComplete JavaScript Module Set:")
    print("✓ main.js - Core functionality and initialization")
    print("✓ chat.js - Chat interface and messaging")
    print("✓ websocket.js - Real-time WebSocket connections")
    print("✓ search.js - Advanced search functionality")
    print("✓ filters.js - Data filtering and sorting")
    print("✓ autocomplete.js - Smart input suggestions")
    print("✓ bulk-actions.js - Bulk operations")
    print("✓ export.js - Data export capabilities")
    print("✓ image-handler.js - Image processing")
    print("✓ utils.js - Utility functions and modals")
    
    print("\nYour local Reddit chat application now has:")
    print("🎯 Complete frontend functionality")
    print("🎯 Professional user experience")
    print("🎯 Advanced features like bulk operations and export")
    print("🎯 Modern image handling with drag & drop")
    print("🎯 Real-time messaging with WebSocket")
    print("🎯 Comprehensive search and filtering")

if __name__ == "__main__":
    create_remaining_js_files()