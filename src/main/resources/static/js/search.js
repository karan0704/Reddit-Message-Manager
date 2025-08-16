// Search functionality
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
