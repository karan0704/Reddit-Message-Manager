// Chat functionality
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
