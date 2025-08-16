// WebSocket functionality
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
