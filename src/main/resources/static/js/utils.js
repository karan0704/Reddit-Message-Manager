// Utility functions
console.log('Utils module loaded');

/**
 * Show loading indicator
 */
function showLoading(container, message = 'Loading...') {
    if (typeof container === 'string') {
        container = document.getElementById(container);
    }
    
    if (container) {
        container.innerHTML = `
            <div class="loading">
                <div class="spinner"></div>
                <span>${message}</span>
            </div>
        `;
    }
}

/**
 * Show new chat modal
 */
function showNewChatModal() {
    const modalHtml = `
        <div class="modal-overlay">
            <div class="modal modal-medium">
                <div class="modal-header">
                    <h3 class="modal-title">Start New Chat</h3>
                    <button class="modal-close" onclick="closeModal()">&times;</button>
                </div>
                <div class="modal-body">
                    <div class="user-search-container">
                        <input type="text" id="newChatUserSearch" class="user-search-input" 
                               placeholder="Enter username..." autocomplete="off">
                    </div>
                </div>
                <div class="modal-footer">
                    <button onclick="closeModal()" class="btn btn-secondary">Cancel</button>
                    <button onclick="startNewChat()" class="btn btn-primary">Start Chat</button>
                </div>
            </div>
        </div>
    `;
    
    document.body.insertAdjacentHTML('beforeend', modalHtml);
    setTimeout(() => document.querySelector('.modal-overlay').classList.add('show'), 10);
    
    // Focus on input
    document.getElementById('newChatUserSearch').focus();
}

/**
 * Close modal
 */
function closeModal() {
    const overlay = document.querySelector('.modal-overlay');
    if (overlay) {
        overlay.classList.remove('show');
        setTimeout(() => overlay.remove(), 300);
    }
}

/**
 * Start new chat
 */
async function startNewChat() {
    const usernameInput = document.getElementById('newChatUserSearch');
    const username = usernameInput.value.trim();
    
    if (!username) {
        showNotification('Please enter a username', 'error');
        return;
    }
    
    try {
        const response = await fetch(`${CONFIG.API_BASE_URL}/chat/start`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ otherUsername: username })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            closeModal();
            await loadUserChats();
            openChat(data.chat.id);
            showNotification(`Started chat with ${username}`, 'success');
        } else {
            throw new Error(data.error || 'Failed to start chat');
        }
        
    } catch (error) {
        console.error('Error starting chat:', error);
        showNotification('Failed to start chat', 'error');
    }
}

/**
 * Handle search input
 */
function handleSearchInput(e) {
    const query = e.target.value.trim();
    
    if (query.length === 0) {
        return;
    }
    
    if (query.length < 2) {
        return;
    }
    
    clearTimeout(this.searchTimeout);
    this.searchTimeout = setTimeout(() => {
        performSearch(query);
    }, 300);
}

/**
 * Perform search
 */
async function performSearch(query) {
    try {
        const response = await fetch(`${CONFIG.API_BASE_URL}/search/messages?q=${encodeURIComponent(query)}`);
        const data = await response.json();
        
        if (response.ok) {
            displaySearchResults(data);
        }
    } catch (error) {
        console.error('Search error:', error);
    }
}

/**
 * Display search results
 */
function displaySearchResults(results) {
    console.log('Search results:', results);
    // Implement search results display
}

/**
 * Handle message input keydown
 */
function handleMessageInput(e) {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        sendMessage();
    }
}

/**
 * Handle typing indicator
 */
function handleTypingIndicator(e) {
    if (!currentChat || !socket || !isConnected) return;
    
    const messageText = e.target.value.trim();
    
    clearTimeout(typingTimer);
    
    if (messageText.length > 0) {
        sendTypingIndicator(true);
        
        typingTimer = setTimeout(() => {
            sendTypingIndicator(false);
        }, CONFIG.TYPING_TIMEOUT);
    } else {
        sendTypingIndicator(false);
    }
}

/**
 * Send typing indicator via WebSocket
 */
function sendTypingIndicator(isTyping) {
    if (!socket || !isConnected || !currentChat) return;
    
    const message = {
        type: 'typing',
        chatId: currentChat.id,
        isTyping: isTyping
    };
    
    socket.send(JSON.stringify(message));
}

/**
 * Handle window focus
 */
function handleWindowFocus() {
    if (currentChat) {
        markChatAsRead(currentChat.id);
    }
}

/**
 * Handle window blur
 */
function handleWindowBlur() {
    if (typingTimer) {
        clearTimeout(typingTimer);
        sendTypingIndicator(false);
    }
}

/**
 * Handle before unload
 */
function handleBeforeUnload() {
    if (socket && isConnected) {
        socket.close();
    }
}

/**
 * Setup keyboard shortcuts
 */
function setupKeyboardShortcuts() {
    document.addEventListener('keydown', function(e) {
        if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA') {
            return;
        }
        
        if (e.ctrlKey || e.metaKey) {
            switch (e.key) {
                case 'k':
                    e.preventDefault();
                    focusSearch();
                    break;
                case 'n':
                    e.preventDefault();
                    showNewChatModal();
                    break;
            }
        }
    });
}

/**
 * Focus search input
 */
function focusSearch() {
    const searchInput = document.getElementById('mainSearchInput') || 
                       document.getElementById('chatSearch');
    if (searchInput) {
        searchInput.focus();
        searchInput.select();
    }
}

/**
 * Initialize tooltips
 */
function initializeTooltips() {
    document.querySelectorAll('[title]').forEach(element => {
        element.addEventListener('mouseenter', showTooltip);
        element.addEventListener('mouseleave', hideTooltip);
    });
}

/**
 * Show tooltip
 */
function showTooltip(e) {
    const tooltip = document.createElement('div');
    tooltip.className = 'tooltip';
    tooltip.textContent = e.target.title;
    
    e.target.setAttribute('data-title', e.target.title);
    e.target.removeAttribute('title');
    
    document.body.appendChild(tooltip);
    
    const rect = e.target.getBoundingClientRect();
    tooltip.style.left = rect.left + (rect.width / 2) - (tooltip.offsetWidth / 2) + 'px';
    tooltip.style.top = rect.top - tooltip.offsetHeight - 8 + 'px';
    
    setTimeout(() => tooltip.classList.add('show'), 100);
}

/**
 * Hide tooltip
 */
function hideTooltip(e) {
    const tooltip = document.querySelector('.tooltip');
    if (tooltip) {
        tooltip.remove();
    }
    
    if (e.target.getAttribute('data-title')) {
        e.target.title = e.target.getAttribute('data-title');
        e.target.removeAttribute('data-title');
    }
}

/**
 * Update user info in UI
 */
function updateUserInfo(userData) {
    const usernameElements = document.querySelectorAll('.username');
    usernameElements.forEach(el => {
        el.textContent = userData.displayName || userData.username;
    });
    
    const avatarElements = document.querySelectorAll('.user-avatar');
    avatarElements.forEach(el => {
        if (userData.avatarUrl) {
            el.src = userData.avatarUrl;
        }
    });
}

/**
 * Handle search keydown
 */
function handleSearchKeydown(e) {
    if (e.key === 'Enter') {
        e.preventDefault();
        const query = e.target.value.trim();
        if (query) {
            performSearch(query);
        }
    }
    
    if (e.key === 'Escape') {
        e.target.value = '';
    }
}

// Export utility functions
window.ChatApp = {
    ...window.ChatApp,
    showLoading,
    showNewChatModal,
    handleSearchInput,
    handleMessageInput,
    handleTypingIndicator,
    handleWindowFocus,
    handleWindowBlur,
    handleBeforeUnload,
    setupKeyboardShortcuts,
    updateUserInfo,
    handleSearchKeydown
};

console.log('Utils module loaded successfully');
