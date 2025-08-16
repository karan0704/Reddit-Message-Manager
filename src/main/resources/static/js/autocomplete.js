// Autocomplete functionality
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
