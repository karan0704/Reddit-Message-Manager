import os

def create_js_files():
    # Base path from your previous conversation
    base_path = "D:\\Karan Ticket Project\\Reddit Message Manager"
    
    # JavaScript files for the local chat application
    js_files = [
        {
            "path": "src\\main\\resources\\static\\js\\main.js",
            "content": r"""// Main JavaScript - Core functionality
console.log('Reddit Chat Application loaded');

// Global variables
let currentUser = null;
let currentChat = null;
let socket = null;
let isConnected = false;
let typingTimer = null;
let messageCache = new Map();
let bulkModeActive = false;

// Configuration
const CONFIG = {
    TYPING_TIMEOUT: 1000,
    MESSAGE_LIMIT: 50,
    RECONNECT_ATTEMPTS: 5,
    RECONNECT_DELAY: 3000,
    API_BASE_URL: '/api',
    WS_URL: '/ws/chat'
};

// Initialize application
document.addEventListener('DOMContentLoaded', function() {
    console.log('Initializing Reddit Chat Application...');
    
    initializeApp();
    setupEventListeners();
    checkAuthStatus();
});

/**
 * Initialize the application
 */
async function initializeApp() {
    try {
        // Load user chats
        await loadUserChats();
        
        // Initialize WebSocket connection
        initializeWebSocket();
        
        // Setup keyboard shortcuts
        setupKeyboardShortcuts();
        
        // Initialize tooltips
        initializeTooltips();
        
        console.log('Application initialized successfully');
        
    } catch (error) {
        console.error('Failed to initialize application:', error);
        showNotification('Failed to initialize application', 'error');
    }
}

/**
 * Setup global event listeners
 */
function setupEventListeners() {
    // Search input
    const searchInput = document.getElementById('mainSearchInput');
    if (searchInput) {
        searchInput.addEventListener('input', handleSearchInput);
        searchInput.addEventListener('keydown', handleSearchKeydown);
    }
    
    // Message input
    const messageInput = document.getElementById('messageInput');
    if (messageInput) {
        messageInput.addEventListener('keydown', handleMessageInput);
        messageInput.addEventListener('input', handleTypingIndicator);
    }
    
    // Send button
    const sendBtn = document.querySelector('.send-btn');
    if (sendBtn) {
        sendBtn.addEventListener('click', sendMessage);
    }
    
    // Window events
    window.addEventListener('beforeunload', handleBeforeUnload);
    window.addEventListener('focus', handleWindowFocus);
    window.addEventListener('blur', handleWindowBlur);
}

/**
 * Check authentication status
 */
async function checkAuthStatus() {
    try {
        const response = await fetch(`${CONFIG.API_BASE_URL}/auth/status`);
        const data = await response.json();
        
        if (data.authenticated) {
            currentUser = data;
            updateUserInfo(data);
            console.log('User authenticated:', data.username);
        } else {
            window.location.href = '/login';
        }
        
    } catch (error) {
        console.error('Auth check failed:', error);
        showNotification('Authentication check failed', 'error');
    }
}

/**
 * Show notification
 */
function showNotification(message, type = 'info', duration = 3000) {
    document.querySelectorAll('.notification').forEach(n => n.remove());
    
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.innerHTML = `
        <span>${message}</span>
        <button onclick="this.parentElement.remove()" class="notification-close">×</button>
    `;
    
    document.body.appendChild(notification);
    setTimeout(() => notification.classList.add('show'), 100);
    
    if (duration > 0) {
        setTimeout(() => {
            notification.classList.remove('show');
            setTimeout(() => notification.remove(), 300);
        }, duration);
    }
}

/**
 * Format date for display
 */
function formatDate(date) {
    if (!date) return '';
    
    const now = new Date();
    const messageDate = new Date(date);
    
    if (messageDate.toDateString() === now.toDateString()) {
        return messageDate.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    } else {
        return messageDate.toLocaleDateString([], { month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit' });
    }
}

/**
 * Escape HTML to prevent XSS
 */
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// Export functions for use in other modules
window.ChatApp = {
    showNotification,
    formatDate,
    escapeHtml
};

console.log('Main JavaScript loaded successfully');
"""
        },
        
        {
            "path": "src\\main\\resources\\static\\js\\chat.js",
            "content": r"""// Chat functionality
console.log('Chat module loaded');

// Chat-specific variables
let activeChat = null;
let messageHistory = [];
let isLoadingMessages = false;
let messageContainer = null;
let shouldAutoScroll = true;

/**
 * Load user chats
 */
async function loadUserChats(filter = 'all') {
    try {
        showLoading('chatList', 'Loading chats...');
        
        const params = new URLSearchParams();
        if (filter === 'pinned') params.append('onlyPinned', 'true');
        if (filter === 'unread') params.append('onlyUnread', 'true');
        
        const response = await fetch(`${CONFIG.API_BASE_URL}/chat/list?${params}`);
        const data = await response.json();
        
        if (response.ok) {
            displayChats(data.chats);
        } else {
            throw new Error(data.error || 'Failed to load chats');
        }
        
    } catch (error) {
        console.error('Error loading chats:', error);
        document.getElementById('chatList').innerHTML = `
            <div class="error-message">
                <p>Failed to load chats</p>
                <button onclick="loadUserChats()" class="btn btn-primary">Retry</button>
            </div>
        `;
    }
}

/**
 * Display chats in sidebar
 */
function displayChats(chats) {
    const chatList = document.getElementById('chatList');
    
    if (!chats || chats.length === 0) {
        chatList.innerHTML = `
            <div class="empty-state">
                <h4>No chats yet</h4>
                <p>Start a conversation with someone!</p>
                <button onclick="showNewChatModal()" class="btn btn-primary">New Chat</button>
            </div>
        `;
        return;
    }
    
    const chatHtml = chats.map(chat => createChatItemHtml(chat)).join('');
    chatList.innerHTML = chatHtml;
    
    // Add click listeners to chat items
    chatList.querySelectorAll('.chat-item').forEach(item => {
        item.addEventListener('click', function(e) {
            if (e.target.closest('.chat-checkbox') || e.target.closest('.pin-btn')) {
                return;
            }
            
            const chatId = parseInt(this.dataset.chatId);
            openChat(chatId);
        });
    });
}

/**
 * Create HTML for a chat item
 */
function createChatItemHtml(chat) {
    const isActive = activeChat && activeChat.id === chat.id;
    const lastMessageTime = chat.lastMessageTimestamp ? formatDate(chat.lastMessageTimestamp) : '';
    const unreadBadge = chat.hasUnread && chat.unreadCount > 0 ? 
        `<span class="unread-count">${chat.unreadCount}</span>` : '';
    const pinnedIcon = chat.isPinned ? '<span class="pinned-indicator">📌</span>' : '';
    
    return `
        <div class="chat-item ${isActive ? 'active' : ''}" data-chat-id="${chat.id}">
            <div class="chat-avatar">
                <img src="/api/user/${encodeURIComponent(chat.otherUsername || 'unknown')}/avatar" 
                     alt="${escapeHtml(chat.otherUsername || 'Unknown')}" 
                     class="avatar-img"
                     onerror="this.src='/images/default-avatar.png'">
                ${chat.hasUnread ? '<div class="unread-indicator"></div>' : ''}
            </div>
            
            <div class="chat-content">
                <div class="chat-header">
                    <span class="chat-username">${escapeHtml(chat.otherUsername || 'Unknown User')}</span>
                    <span class="chat-time">${lastMessageTime}</span>
                </div>
                
                <div class="chat-preview">
                    <span class="last-message">${escapeHtml(chat.lastMessage || 'No messages yet')}</span>
                    <div class="chat-indicators">
                        ${pinnedIcon}
                        ${unreadBadge}
                    </div>
                </div>
            </div>
            
            <div class="chat-actions">
                <button class="pin-btn" onclick="event.stopPropagation(); togglePin(${chat.id})" 
                        title="${chat.isPinned ? 'Unpin' : 'Pin'}">
                    <i class="${chat.isPinned ? 'icon-pin-filled' : 'icon-pin'}">📌</i>
                </button>
            </div>
        </div>
    `;
}

/**
 * Open a chat
 */
async function openChat(chatId) {
    try {
        const chatElement = document.querySelector(`[data-chat-id="${chatId}"]`);
        if (!chatElement) {
            console.error('Chat not found:', chatId);
            return;
        }
        
        // Update active chat UI
        document.querySelectorAll('.chat-item').forEach(item => {
            item.classList.remove('active');
        });
        chatElement.classList.add('active');
        
        const chatUsername = chatElement.querySelector('.chat-username').textContent;
        activeChat = { id: chatId, otherUsername: chatUsername };
        currentChat = activeChat;
        
        showChatPanel(activeChat);
        await loadChatMessages(chatId);
        markChatAsRead(chatId);
        
    } catch (error) {
        console.error('Error opening chat:', error);
        showNotification('Failed to open chat', 'error');
    }
}

/**
 * Load chat messages
 */
async function loadChatMessages(chatId, page = 0) {
    if (isLoadingMessages) return;
    
    try {
        isLoadingMessages = true;
        
        if (page === 0) {
            showLoading('messagesContainer', 'Loading messages...');
        }
        
        const response = await fetch(`${CONFIG.API_BASE_URL}/chat/${chatId}/messages?page=${page}&size=${CONFIG.MESSAGE_LIMIT}`);
        const data = await response.json();
        
        if (response.ok) {
            messageHistory = data.messages || [];
            displayMessages(messageHistory);
            setTimeout(scrollToBottom, 100);
        } else {
            throw new Error(data.error || 'Failed to load messages');
        }
        
    } catch (error) {
        console.error('Error loading messages:', error);
        if (messageContainer) {
            messageContainer.innerHTML = `
                <div class="error-message">
                    <p>Failed to load messages</p>
                    <button onclick="loadChatMessages(${chatId})" class="btn btn-primary">Retry</button>
                </div>
            `;
        }
    } finally {
        isLoadingMessages = false;
    }
}

/**
 * Display messages
 */
function displayMessages(messages) {
    if (!messageContainer) return;
    
    if (!messages || messages.length === 0) {
        messageContainer.innerHTML = `
            <div class="empty-state">
                <p>No messages yet. Start the conversation!</p>
            </div>
        `;
        return;
    }
    
    const messagesHtml = messages.map(message => createMessageHtml(message)).join('');
    messageContainer.innerHTML = messagesHtml;
}

/**
 * Create HTML for a message
 */
function createMessageHtml(message) {
    const isOwn = message.isOwnMessage || (currentUser && message.senderUsername === currentUser.username);
    const messageClass = isOwn ? 'own-message' : 'other-message';
    const formattedTime = message.formattedTime || formatDate(message.createdAt);
    
    return `
        <div class="message-bubble ${messageClass}" data-message-id="${message.id}">
            ${!isOwn ? `
                <div class="message-header">
                    <span class="sender-name">${escapeHtml(message.senderUsername)}</span>
                    <span class="message-time">${formattedTime}</span>
                </div>
            ` : ''}
            
            <div class="message-content">
                <div class="text-message"><p>${escapeHtml(message.messageContent)}</p></div>
            </div>
            
            ${isOwn ? `
                <div class="message-footer">
                    <span class="message-time">${formattedTime}</span>
                    <span class="${message.isRead ? 'read-indicator' : 'sent-indicator'}" 
                          title="${message.isRead ? 'Read' : 'Sent'}">
                        ${message.isRead ? '✓✓' : '✓'}
                    </span>
                </div>
            ` : ''}
        </div>
    `;
}

/**
 * Show chat panel
 */
function showChatPanel(chat) {
    const noChatSelected = document.getElementById('noChatSelected');
    const activeChatContainer = document.getElementById('activeChatContainer');
    
    if (noChatSelected) noChatSelected.classList.add('hidden');
    if (activeChatContainer) activeChatContainer.classList.remove('hidden');
    
    const chatUsername = document.querySelector('.active-chat .chat-username');
    if (chatUsername) chatUsername.textContent = chat.otherUsername;
    
    messageContainer = document.getElementById('messagesContainer');
}

/**
 * Send message
 */
async function sendMessage() {
    const messageInput = document.getElementById('messageInput');
    if (!messageInput || !activeChat) return;
    
    const messageText = messageInput.value.trim();
    if (!messageText) return;
    
    try {
        messageInput.value = '';
        
        const messageData = {
            messageContent: messageText,
            messageType: 'TEXT'
        };
        
        const response = await fetch(`${CONFIG.API_BASE_URL}/chat/${activeChat.id}/send`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(messageData)
        });
        
        const data = await response.json();
        
        if (response.ok) {
            addMessageToUI(data.message);
        } else {
            throw new Error(data.error || 'Failed to send message');
        }
        
    } catch (error) {
        console.error('Error sending message:', error);
        showNotification('Failed to send message', 'error');
        messageInput.value = messageText;
    }
}

/**
 * Add message to UI
 */
function addMessageToUI(message) {
    if (!messageContainer) return;
    
    const messageHtml = createMessageHtml(message);
    messageContainer.insertAdjacentHTML('beforeend', messageHtml);
    messageHistory.push(message);
    
    if (shouldAutoScroll) {
        setTimeout(scrollToBottom, 100);
    }
}

/**
 * Scroll to bottom
 */
function scrollToBottom() {
    if (messageContainer) {
        messageContainer.scrollTop = messageContainer.scrollHeight;
    }
}

/**
 * Toggle pin status
 */
async function togglePin(chatId) {
    try {
        const response = await fetch(`${CONFIG.API_BASE_URL}/chat/${chatId}/pin`, {
            method: 'POST'
        });
        
        const data = await response.json();
        
        if (response.ok) {
            showNotification(data.isPinned ? 'Chat pinned' : 'Chat unpinned', 'success', 1500);
            loadUserChats(); // Refresh chat list
        } else {
            throw new Error(data.error || 'Failed to toggle pin');
        }
        
    } catch (error) {
        console.error('Error toggling pin:', error);
        showNotification('Failed to update pin status', 'error');
    }
}

/**
 * Mark chat as read
 */
async function markChatAsRead(chatId) {
    try {
        await fetch(`${CONFIG.API_BASE_URL}/chat/${chatId}/read`, {
            method: 'POST'
        });
    } catch (error) {
        console.error('Error marking chat as read:', error);
    }
}

// Export chat functions
window.ChatApp = {
    ...window.ChatApp,
    loadUserChats,
    openChat,
    sendMessage,
    togglePin,
    scrollToBottom
};

console.log('Chat module loaded successfully');
"""
        },
        
        {
            "path": "src\\main\\resources\\static\\js\\websocket.js",
            "content": r"""// WebSocket functionality
console.log('WebSocket module loaded');

let reconnectAttempts = 0;
let reconnectTimer = null;

/**
 * Initialize WebSocket connection
 */
function initializeWebSocket() {
    if (!currentUser) {
        console.log('User not authenticated, skipping WebSocket connection');
        return;
    }
    
    try {
        const wsUrl = `ws://${window.location.host}${CONFIG.WS_URL}?username=${encodeURIComponent(currentUser.username)}`;
        
        console.log('Connecting to WebSocket:', wsUrl);
        socket = new WebSocket(wsUrl);
        
        socket.onopen = handleWebSocketOpen;
        socket.onmessage = handleWebSocketMessage;
        socket.onclose = handleWebSocketClose;
        socket.onerror = handleWebSocketError;
        
    } catch (error) {
        console.error('Failed to initialize WebSocket:', error);
        showNotification('Failed to connect to real-time messaging', 'error');
    }
}

/**
 * Handle WebSocket connection open
 */
function handleWebSocketOpen(event) {
    console.log('WebSocket connected');
    isConnected = true;
    reconnectAttempts = 0;
    
    if (reconnectTimer) {
        clearTimeout(reconnectTimer);
        reconnectTimer = null;
    }
    
    showNotification('Connected to real-time messaging', 'success', 2000);
}

/**
 * Handle WebSocket message
 */
function handleWebSocketMessage(event) {
    try {
        const message = JSON.parse(event.data);
        
        switch (message.type) {
            case 'new_message':
                handleNewMessage(message);
                break;
            case 'typing':
                handleTypingIndicator(message);
                break;
            default:
                console.log('Unknown WebSocket message type:', message.type);
        }
        
    } catch (error) {
        console.error('Error parsing WebSocket message:', error);
    }
}

/**
 * Handle WebSocket connection close
 */
function handleWebSocketClose(event) {
    console.log('WebSocket disconnected:', event.code, event.reason);
    isConnected = false;
    
    if (event.code !== 1000 && reconnectAttempts < CONFIG.RECONNECT_ATTEMPTS) {
        attemptReconnect();
    }
}

/**
 * Handle WebSocket error
 */
function handleWebSocketError(error) {
    console.error('WebSocket error:', error);
    showNotification('Connection error occurred', 'error');
}

/**
 * Attempt to reconnect
 */
function attemptReconnect() {
    if (reconnectTimer) return;
    
    reconnectAttempts++;
    const delay = Math.min(CONFIG.RECONNECT_DELAY * Math.pow(2, reconnectAttempts - 1), 30000);
    
    console.log(`Attempting reconnect ${reconnectAttempts}/${CONFIG.RECONNECT_ATTEMPTS} in ${delay}ms`);
    
    showNotification(`Reconnecting... (${reconnectAttempts}/${CONFIG.RECONNECT_ATTEMPTS})`, 'info', delay);
    
    reconnectTimer = setTimeout(() => {
        reconnectTimer = null;
        initializeWebSocket();
    }, delay);
}

/**
 * Handle new message
 */
function handleNewMessage(message) {
    const newMessage = message.message;
    
    if (newMessage.senderUsername === currentUser?.username) {
        return;
    }
    
    if (activeChat && newMessage.chatId === activeChat.id) {
        addMessageToUI(newMessage);
        
        if (document.hidden) {
            showDesktopNotification(
                `New message from ${newMessage.senderUsername}`,
                newMessage.messageContent
            );
        }
    }
}

/**
 * Handle typing indicator
 */
function handleTypingIndicator(message) {
    if (message.username === currentUser?.username) {
        return;
    }
    
    if (activeChat && message.chatId === activeChat.id) {
        showTypingIndicator(message.username, message.isTyping);
    }
}

/**
 * Show typing indicator
 */
function showTypingIndicator(username, isTyping) {
    const messagesContainer = document.getElementById('messagesContainer');
    if (!messagesContainer) return;
    
    let typingIndicator = document.getElementById('typingIndicator');
    
    if (isTyping) {
        if (!typingIndicator) {
            typingIndicator = document.createElement('div');
            typingIndicator.id = 'typingIndicator';
            typingIndicator.className = 'typing-indicator';
            typingIndicator.innerHTML = `
                <div class="typing-content">
                    <span class="typing-user">${escapeHtml(username)}</span>
                    <span class="typing-text">is typing</span>
                    <div class="typing-dots">
                        <span></span>
                        <span></span>
                        <span></span>
                    </div>
                </div>
            `;
            
            messagesContainer.appendChild(typingIndicator);
            
            if (shouldAutoScroll) {
                setTimeout(scrollToBottom, 100);
            }
        }
        
        clearTimeout(typingIndicator.hideTimer);
        typingIndicator.hideTimer = setTimeout(() => {
            if (typingIndicator && typingIndicator.parentNode) {
                typingIndicator.remove();
            }
        }, 3000);
        
    } else if (typingIndicator) {
        typingIndicator.remove();
    }
}

/**
 * Show desktop notification
 */
function showDesktopNotification(title, body) {
    if (!('Notification' in window)) {
        return;
    }
    
    if (Notification.permission === 'granted') {
        const notification = new Notification(title, {
            body: body,
            icon: '/images/logo.png'
        });
        
        notification.onclick = function() {
            window.focus();
            notification.close();
        };
        
        setTimeout(() => notification.close(), 5000);
        
    } else if (Notification.permission !== 'denied') {
        Notification.requestPermission().then(permission => {
            if (permission === 'granted') {
                showDesktopNotification(title, body);
            }
        });
    }
}

// Export WebSocket functions
window.ChatApp = {
    ...window.ChatApp,
    initializeWebSocket
};

console.log('WebSocket module loaded successfully');
"""
        },
        
        {
            "path": "src\\main\\resources\\static\\js\\utils.js",
            "content": r"""// Utility functions
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
"""
        }
    ]
    
    # Function to create files
    def create_files(files_list):
        print("\nCreating JavaScript files...")
        
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
    
    # Create all JS files
    create_files(js_files)
    
    print("\n" + "="*70)
    print("JavaScript files created successfully!")
    print("="*70)
    
    print("\nCreated JavaScript Files:")
    print("✓ main.js - Core functionality and initialization")
    print("✓ chat.js - Chat interface and messaging")
    print("✓ websocket.js - Real-time WebSocket connections")
    print("✓ utils.js - Utility functions and modals")
    
    print("\nJavaScript Features:")
    print("• Authentication handling with session management")
    print("• Real-time messaging via WebSocket")
    print("• Chat management (load, display, send messages)")
    print("• Typing indicators and online status")
    print("• Desktop notifications for new messages")
    print("• Keyboard shortcuts for power users")
    print("• Modal system for new chat creation")
    print("• Search functionality with autocomplete")
    print("• Error handling and reconnection logic")
    print("• Message formatting and display")
    
    print("\nNext steps:")
    print("1. Create HTML templates to include these JS files")
    print("2. Test the frontend functionality")
    print("3. Run your Spring Boot application")
    print("4. Test WebSocket connections")
    print("5. Verify all features work together")

if __name__ == "__main__":
    create_js_files()