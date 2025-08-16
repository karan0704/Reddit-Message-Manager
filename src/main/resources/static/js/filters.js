// Filter functionality
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
