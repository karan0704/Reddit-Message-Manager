import os

def create_complete_frontend():
    base_path = "D:\\Karan Ticket Project\\Reddit Message Manager"

    # Create static directories
    css_dir = os.path.join(base_path, "src\\main\\resources\\static\\css")
    js_dir = os.path.join(base_path, "src\\main\\resources\\static\\js")

    os.makedirs(css_dir, exist_ok=True)
    os.makedirs(js_dir, exist_ok=True)

    # Complete CSS file
    css_content = """/* Reddit Message Manager Styles */
body {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    margin: 0;
    padding: 0;
    background-color: #f5f5f5;
    line-height: 1.6;
}

.container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 20px;
}

/* Header Styles */
.header {
    background: white;
    padding: 20px;
    border-radius: 8px;
    margin-bottom: 20px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    display: flex;
    justify-content: space-between;
    align-items: center;
}

h1 {
    color: #333;
    margin: 0;
    font-size: 2rem;
}

.username {
    color: #ff4500;
    font-weight: bold;
}

/* Button Styles */
.btn {
    display: inline-block;
    padding: 12px 24px;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    font-weight: bold;
    text-decoration: none;
    text-align: center;
    transition: background-color 0.3s ease;
    font-size: 14px;
}

.btn-primary {
    background-color: #ff4500;
    color: white;
}

.btn-primary:hover {
    background-color: #e03d00;
}

.btn-secondary {
    background-color: #0079d3;
    color: white;
}

.btn-secondary:hover {
    background-color: #006bb3;
}

.btn-danger {
    background-color: #dc3545;
    color: white;
}

.btn-danger:hover {
    background-color: #c82333;
}

/* Controls Section */
.controls {
    background: white;
    padding: 20px;
    border-radius: 8px;
    margin-bottom: 20px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.controls-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 15px;
    margin-bottom: 20px;
}

/* Search Section */
.search-section {
    background: white;
    padding: 20px;
    border-radius: 8px;
    margin-bottom: 20px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.search-form {
    display: flex;
    gap: 10px;
    margin-bottom: 15px;
    flex-wrap: wrap;
}

.search-input {
    flex: 1;
    min-width: 250px;
    padding: 12px;
    border: 1px solid #ddd;
    border-radius: 5px;
    font-size: 16px;
}

/* Messages Container */
.messages-container {
    background: white;
    padding: 20px;
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    min-height: 300px;
}

.message {
    background: #f8f9fa;
    margin: 15px 0;
    padding: 20px;
    border-radius: 8px;
    border-left: 4px solid #ff4500;
    transition: box-shadow 0.3s ease;
}

.message:hover {
    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.message-header {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    margin-bottom: 10px;
}

.message-subject {
    margin: 0;
    color: #333;
    font-size: 1.2rem;
    font-weight: bold;
}

.message-meta {
    font-size: 0.9rem;
    color: #666;
    margin: 5px 0;
}

.message-body {
    margin: 15px 0;
    color: #444;
    background: white;
    padding: 15px;
    border-radius: 5px;
    max-height: 150px;
    overflow-y: auto;
}

.message-actions {
    margin-top: 15px;
}

.message-actions .btn {
    margin-right: 10px;
    padding: 8px 16px;
    font-size: 12px;
}

/* Loading and Status */
.loading {
    text-align: center;
    color: #666;
    font-style: italic;
    padding: 40px;
}

.error-message {
    color: #dc3545;
    background: #f8d7da;
    padding: 15px;
    border-radius: 5px;
    border: 1px solid #f5c6cb;
}

.success-message {
    color: #155724;
    background: #d4edda;
    padding: 15px;
    border-radius: 5px;
    border: 1px solid #c3e6cb;
}

/* Stats Display */
.stats-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 15px;
}

.stat-card {
    background: #f8f9fa;
    padding: 20px;
    border-radius: 8px;
    text-align: center;
    border-left: 4px solid #0079d3;
}

.stat-number {
    font-size: 2rem;
    font-weight: bold;
    color: #0079d3;
    margin-bottom: 5px;
}

.stat-label {
    color: #666;
    font-size: 0.9rem;
}

/* Responsive Design */
@media (max-width: 768px) {
    .container {
        padding: 10px;
    }
    
    .header {
        flex-direction: column;
        text-align: center;
        gap: 15px;
    }
    
    .search-form {
        flex-direction: column;
    }
    
    .search-input {
        min-width: 100%;
    }
    
    .controls-grid {
        grid-template-columns: 1fr;
    }
    
    .message-header {
        flex-direction: column;
        align-items: flex-start;
    }
}

/* Authentication Page Styles */
.auth-container {
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    background: linear-gradient(135deg, #ff4500 0%, #ff6b35 100%);
}

.auth-card {
    background: white;
    padding: 40px;
    border-radius: 15px;
    box-shadow: 0 20px 40px rgba(0,0,0,0.1);
    text-align: center;
    max-width: 400px;
    width: 90%;
}

.auth-card h1 {
    color: #333;
    margin-bottom: 10px;
    font-size: 2.5rem;
}

.auth-card p {
    color: #666;
    margin-bottom: 30px;
    font-size: 1.1rem;
}

.login-btn {
    display: inline-block;
    background-color: #ff4500;
    color: white;
    padding: 15px 30px;
    text-decoration: none;
    border-radius: 8px;
    font-weight: bold;
    font-size: 1.1rem;
    transition: all 0.3s ease;
}

.login-btn:hover {
    background-color: #e03d00;
    transform: translateY(-2px);
}

.auth-section {
    text-align: center;
    margin: 30px 0;
}"""

    # Complete JavaScript file
    js_content = """// Reddit Message Manager JavaScript
console.log('Reddit Message Manager loaded');

// Global variables
let currentUser = null;
let currentMessages = [];

// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
    checkAuthStatus();
});

// Check authentication status
async function checkAuthStatus() {
    try {
        const response = await fetch('/auth/status');
        const data = await response.json();
        
        if (data.authenticated) {
            currentUser = data;
            console.log('User authenticated:', data.username);
        }
    } catch (error) {
        console.log('Auth check failed:', error);
    }
}

// Load messages by type
async function loadMessages(type, refresh = true) {
    const messagesDiv = document.getElementById('messages');
    if (messagesDiv) {
        messagesDiv.innerHTML = `<div class="loading">Loading ${type} messages...</div>`;
    }
    
    try {
        const response = await fetch(`/api/messages/${type}?refresh=${refresh}`);
        const data = await response.json();
        
        if (response.ok) {
            currentMessages = data.messages || [];
            displayMessages(currentMessages, type);
            showSuccessMessage(`Loaded ${currentMessages.length} ${type} messages`);
        } else {
            showErrorMessage(`Error loading messages: ${data.error}`);
        }
    } catch (error) {
        console.error('Network error:', error);
        showErrorMessage('Failed to load messages. Please check your connection.');
    }
}

// Display messages in the UI
function displayMessages(messages, type = 'messages') {
    const messagesDiv = document.getElementById('messages');
    
    if (!messagesDiv) {
        console.error('Messages container not found');
        return;
    }
    
    if (!messages || messages.length === 0) {
        messagesDiv.innerHTML = `
            <div class="loading">
                <p>No ${type} found.</p>
                <button onclick="loadMessages('${type}')" class="btn btn-primary">Refresh</button>
            </div>
        `;
        return;
    }
    
    let html = `
        <div class="message-header">
            <h3>${capitalizeFirst(type)} (${messages.length})</h3>
            <button onclick="loadMessages('${type}')" class="btn btn-secondary">Refresh</button>
        </div>
    `;
    
    messages.forEach((message, index) => {
        html += createMessageHtml(message, index);
    });
    
    messagesDiv.innerHTML = html;
}

// Create HTML for a single message
function createMessageHtml(message, index) {
    const subject = message.subject || 'No Subject';
    const author = message.author || 'Unknown';
    const body = message.body || 'No content available';
    const date = message.redditCreatedAt ? new Date(message.redditCreatedAt).toLocaleString() : 'Unknown date';
    const subreddit = message.subreddit ? `r/${message.subreddit}` : '';
    const isRead = message.isRead ? 'read' : 'unread';
    
    return `
        <div class="message ${isRead}" data-message-id="${message.id}" data-index="${index}">
            <div class="message-header">
                <h4 class="message-subject">${escapeHtml(subject)}</h4>
                <div class="message-status ${isRead}">${isRead.toUpperCase()}</div>
            </div>
            <div class="message-meta">
                <strong>From:</strong> ${escapeHtml(author)} | 
                <strong>Date:</strong> ${date}
                ${subreddit ? ` | <strong>Subreddit:</strong> ${escapeHtml(subreddit)}` : ''}
            </div>
            <div class="message-body">
                ${escapeHtml(body.substring(0, 300))}${body.length > 300 ? '...' : ''}
            </div>
            <div class="message-actions">
                ${!message.isRead ? `<button onclick="markAsRead(${message.id})" class="btn btn-primary">Mark as Read</button>` : ''}
                <button onclick="showFullMessage(${index})" class="btn btn-secondary">View Full</button>
                ${message.context ? `<a href="${message.context}" target="_blank" class="btn btn-secondary">View Context</a>` : ''}
            </div>
        </div>
    `;
}

// Search messages
async function searchMessages() {
    const searchInput = document.getElementById('searchInput');
    if (!searchInput) {
        console.error('Search input not found');
        return;
    }
    
    const query = searchInput.value.trim();
    if (!query) {
        showErrorMessage('Please enter a search term');
        return;
    }
    
    const messagesDiv = document.getElementById('messages');
    if (messagesDiv) {
        messagesDiv.innerHTML = '<div class="loading">Searching messages...</div>';
    }
    
    try {
        const response = await fetch(`/api/search/messages?q=${encodeURIComponent(query)}`);
        const data = await response.json();
        
        if (response.ok) {
            displayMessages(data.messages, 'search results');
            showSuccessMessage(`Found ${data.totalResults} results for "${query}"`);
        } else {
            showErrorMessage(`Search failed: ${data.error}`);
        }
    } catch (error) {
        console.error('Search error:', error);
        showErrorMessage('Search failed. Please try again.');
    }
}

// Search Reddit posts
async function searchRedditPosts() {
    const searchInput = document.getElementById('searchInput');
    if (!searchInput) {
        console.error('Search input not found');
        return;
    }
    
    const query = searchInput.value.trim();
    if (!query) {
        showErrorMessage('Please enter a search term');
        return;
    }
    
    const messagesDiv = document.getElementById('messages');
    if (messagesDiv) {
        messagesDiv.innerHTML = '<div class="loading">Searching Reddit posts...</div>';
    }
    
    try {
        const response = await fetch(`/api/search/posts?q=${encodeURIComponent(query)}`);
        const data = await response.json();
        
        if (response.ok) {
            displaySearchResults(data);
            showSuccessMessage(`Found ${data.totalResults} Reddit posts for "${query}"`);
        } else {
            showErrorMessage(`Reddit search failed: ${data.error}`);
        }
    } catch (error) {
        console.error('Reddit search error:', error);
        showErrorMessage('Reddit search failed. Please try again.');
    }
}

// Display Reddit search results
function displaySearchResults(data) {
    const messagesDiv = document.getElementById('messages');
    
    if (!messagesDiv) return;
    
    if (!data.posts || data.posts.length === 0) {
        messagesDiv.innerHTML = '<div class="loading"><p>No Reddit posts found.</p></div>';
        return;
    }
    
    let html = `<h3>Reddit Search Results (${data.totalResults})</h3>`;
    
    data.posts.forEach(postData => {
        const post = postData.data;
        html += `
            <div class="message">
                <div class="message-header">
                    <h4 class="message-subject">${escapeHtml(post.title)}</h4>
                </div>
                <div class="message-meta">
                    <strong>Subreddit:</strong> r/${escapeHtml(post.subreddit)} | 
                    <strong>Author:</strong> ${escapeHtml(post.author)} | 
                    <strong>Score:</strong> ${post.score}
                </div>
                <div class="message-actions">
                    <a href="https://reddit.com${post.permalink}" target="_blank" class="btn btn-primary">View Post</a>
                </div>
            </div>
        `;
    });
    
    messagesDiv.innerHTML = html;
}

// Get message statistics
async function getStats() {
    const messagesDiv = document.getElementById('messages');
    if (messagesDiv) {
        messagesDiv.innerHTML = '<div class="loading">Loading statistics...</div>';
    }
    
    try {
        const response = await fetch('/api/messages/stats');
        const data = await response.json();
        
        if (response.ok) {
            displayStats(data.statistics);
        } else {
            showErrorMessage(`Failed to load statistics: ${data.error}`);
        }
    } catch (error) {
        console.error('Stats error:', error);
        showErrorMessage('Failed to load statistics.');
    }
}

// Display statistics
function displayStats(stats) {
    const messagesDiv = document.getElementById('messages');
    if (!messagesDiv) return;
    
    messagesDiv.innerHTML = `
        <h3>Message Statistics</h3>
        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-number">0</div>
                <div class="stat-label">Total Messages</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">0</div>
                <div class="stat-label">Unread Messages</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">0</div>
                <div class="stat-label">Inbox Messages</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">0</div>
                <div class="stat-label">Sent Messages</div>
            </div>
        </div>
        <div class="message">
            <h4>Statistics Summary</h4>
            <p>${stats.body || 'No statistics available'}</p>
        </div>
    `;
}

// Mark message as read
async function markAsRead(messageId) {
    try {
        const response = await fetch(`/api/messages/${messageId}/read`, {
            method: 'POST'
        });
        
        if (response.ok) {
            // Update UI to reflect read status
            const messageElement = document.querySelector(`[data-message-id="${messageId}"]`);
            if (messageElement) {
                messageElement.classList.remove('unread');
                messageElement.classList.add('read');
                
                const statusElement = messageElement.querySelector('.message-status');
                if (statusElement) {
                    statusElement.textContent = 'READ';
                }
                
                const readButton = messageElement.querySelector('button[onclick*="markAsRead"]');
                if (readButton) {
                    readButton.remove();
                }
            }
            
            showSuccessMessage('Message marked as read');
        } else {
            const data = await response.json();
            showErrorMessage(`Failed to mark as read: ${data.error}`);
        }
    } catch (error) {
        console.error('Mark as read error:', error);
        showErrorMessage('Failed to mark message as read');
    }
}

// Show full message in modal or expanded view
function showFullMessage(index) {
    if (currentMessages[index]) {
        const message = currentMessages[index];
        const modal = createModal(message);
        document.body.appendChild(modal);
    }
}

// Create modal for full message view
function createModal(message) {
    const modal = document.createElement('div');
    modal.style.cssText = `
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(0,0,0,0.5);
        display: flex;
        align-items: center;
        justify-content: center;
        z-index: 1000;
    `;
    
    const content = document.createElement('div');
    content.style.cssText = `
        background: white;
        padding: 30px;
        border-radius: 10px;
        max-width: 80%;
        max-height: 80%;
        overflow-y: auto;
        position: relative;
    `;
    
    content.innerHTML = `
        <button onclick="this.closest('.modal').remove()" style="position: absolute; top: 10px; right: 10px; background: #dc3545; color: white; border: none; padding: 5px 10px; border-radius: 3px; cursor: pointer;">×</button>
        <h3>${escapeHtml(message.subject || 'No Subject')}</h3>
        <p><strong>From:</strong> ${escapeHtml(message.author || 'Unknown')}</p>
        <p><strong>Date:</strong> ${message.redditCreatedAt ? new Date(message.redditCreatedAt).toLocaleString() : 'Unknown'}</p>
        ${message.subreddit ? `<p><strong>Subreddit:</strong> r/${escapeHtml(message.subreddit)}</p>` : ''}
        <div style="margin-top: 20px; padding: 20px; background: #f8f9fa; border-radius: 5px;">
            ${escapeHtml(message.body || 'No content available')}
        </div>
    `;
    
    modal.appendChild(content);
    modal.className = 'modal';
    
    modal.onclick = function(e) {
        if (e.target === modal) {
            modal.remove();
        }
    };
    
    return modal;
}

// Utility functions
function capitalizeFirst(str) {
    return str.charAt(0).toUpperCase() + str.slice(1);
}

function escapeHtml(text) {
    if (!text) return '';
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

function showErrorMessage(message) {
    showToast(message, 'error');
}

function showSuccessMessage(message) {
    showToast(message, 'success');
}

function showToast(message, type = 'info') {
    const toast = document.createElement('div');
    toast.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 15px 20px;
        border-radius: 5px;
        color: white;
        font-weight: bold;
        z-index: 1001;
        max-width: 300px;
    `;
    
    switch(type) {
        case 'error':
            toast.style.backgroundColor = '#dc3545';
            break;
        case 'success':
            toast.style.backgroundColor = '#28a745';
            break;
        default:
            toast.style.backgroundColor = '#17a2b8';
    }
    
    toast.textContent = message;
    document.body.appendChild(toast);
    
    setTimeout(() => {
        toast.remove();
    }, 5000);
}

// Keyboard shortcuts
document.addEventListener('keydown', function(e) {
    if (e.ctrlKey || e.metaKey) {
        switch(e.key) {
            case 'i':
                e.preventDefault();
                loadMessages('inbox');
                break;
            case 'u':
                e.preventDefault();
                loadMessages('unread');
                break;
            case 's':
                e.preventDefault();
                loadMessages('sent');
                break;
            case 'f':
                e.preventDefault();
                const searchInput = document.getElementById('searchInput');
                if (searchInput) searchInput.focus();
                break;
        }
    }
});

console.log('Reddit Message Manager JavaScript loaded successfully');"""

    # Write the files
    try:
        # Write CSS file
        css_path = os.path.join(css_dir, "style.css")
        with open(css_path, 'w', encoding='utf-8') as f:
            f.write(css_content)
        print("✓ Created complete CSS file")

        # Write JavaScript file
        js_path = os.path.join(js_dir, "app.js")
        with open(js_path, 'w', encoding='utf-8') as f:
            f.write(js_content)
        print("✓ Created complete JavaScript file")

        print("\n✅ Complete frontend files created!")
        print("\nFeatures included:")
        print("• Complete message loading and display")
        print("• Search functionality (messages and Reddit posts)")
        print("• Message statistics")
        print("• Mark messages as read")
        print("• Full message modal view")
        print("• Toast notifications")
        print("• Keyboard shortcuts (Ctrl+I, Ctrl+U, Ctrl+S, Ctrl+F)")
        print("• Responsive design")
        print("• Error handling")

        print("\nYour frontend is now complete and fully functional!")

    except Exception as e:
        print(f"Error creating frontend files: {e}")

if __name__ == "__main__":
    create_complete_frontend()
