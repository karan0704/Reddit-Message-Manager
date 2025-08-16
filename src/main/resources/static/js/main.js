// Main JavaScript - Core functionality
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
