import os

def create_css_files():
    # Base path from your previous conversation
    base_path = "D:\\Karan Ticket Project\\Reddit Message Manager"

    # CSS files for the local chat application
    css_files = [
        {
            "path": "src\\main\\resources\\static\\css\\main.css",
            "content": """/* Main CSS - Global Styles */
:root {
    --primary-color: #ff4500;
    --primary-hover: #e03d00;
    --secondary-color: #0079d3;
    --secondary-hover: #006bb3;
    --background-color: #f8f9fa;
    --surface-color: #ffffff;
    --text-primary: #1a1a1b;
    --text-secondary: #787c82;
    --border-color: #edeff1;
    --success-color: #28a745;
    --warning-color: #ffc107;
    --danger-color: #dc3545;
    --info-color: #17a2b8;
    --shadow: 0 2px 4px rgba(0,0,0,0.1);
    --shadow-hover: 0 4px 8px rgba(0,0,0,0.15);
    --border-radius: 8px;
    --font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: var(--font-family);
    background-color: var(--background-color);
    color: var(--text-primary);
    line-height: 1.6;
    overflow-x: hidden;
}

/* Typography */
h1, h2, h3, h4, h5, h6 {
    font-weight: 600;
    margin-bottom: 0.5rem;
    color: var(--text-primary);
}

h1 { font-size: 2rem; }
h2 { font-size: 1.75rem; }
h3 { font-size: 1.5rem; }
h4 { font-size: 1.25rem; }
h5 { font-size: 1.1rem; }
h6 { font-size: 1rem; }

p {
    margin-bottom: 1rem;
    color: var(--text-secondary);
}

a {
    color: var(--secondary-color);
    text-decoration: none;
    transition: color 0.3s ease;
}

a:hover {
    color: var(--secondary-hover);
}

/* Button Styles */
.btn {
    display: inline-block;
    padding: 0.5rem 1rem;
    border: none;
    border-radius: var(--border-radius);
    cursor: pointer;
    font-size: 0.875rem;
    font-weight: 600;
    text-align: center;
    text-decoration: none;
    transition: all 0.3s ease;
    white-space: nowrap;
    user-select: none;
}

.btn-primary {
    background-color: var(--primary-color);
    color: white;
}

.btn-primary:hover {
    background-color: var(--primary-hover);
    transform: translateY(-1px);
    box-shadow: var(--shadow-hover);
}

.btn-secondary {
    background-color: var(--secondary-color);
    color: white;
}

.btn-secondary:hover {
    background-color: var(--secondary-hover);
    transform: translateY(-1px);
    box-shadow: var(--shadow-hover);
}

.btn-success {
    background-color: var(--success-color);
    color: white;
}

.btn-warning {
    background-color: var(--warning-color);
    color: var(--text-primary);
}

.btn-danger {
    background-color: var(--danger-color);
    color: white;
}

.btn-outline {
    background-color: transparent;
    border: 2px solid var(--primary-color);
    color: var(--primary-color);
}

.btn-outline:hover {
    background-color: var(--primary-color);
    color: white;
}

.btn-small {
    padding: 0.25rem 0.5rem;
    font-size: 0.75rem;
}

.btn-large {
    padding: 0.75rem 1.5rem;
    font-size: 1rem;
}

/* Form Controls */
input[type="text"],
input[type="email"],
input[type="password"],
input[type="search"],
input[type="date"],
textarea,
select {
    width: 100%;
    padding: 0.5rem 0.75rem;
    border: 2px solid var(--border-color);
    border-radius: var(--border-radius);
    font-size: 0.875rem;
    transition: border-color 0.3s ease, box-shadow 0.3s ease;
    background-color: var(--surface-color);
    color: var(--text-primary);
}

input[type="text"]:focus,
input[type="email"]:focus,
input[type="password"]:focus,
input[type="search"]:focus,
input[type="date"]:focus,
textarea:focus,
select:focus {
    outline: none;
    border-color: var(--primary-color);
    box-shadow: 0 0 0 3px rgba(255, 69, 0, 0.1);
}

/* Container and Layout */
.container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 1rem;
}

.row {
    display: flex;
    flex-wrap: wrap;
    margin: -0.5rem;
}

.col {
    flex: 1;
    padding: 0.5rem;
}

/* Card Component */
.card {
    background-color: var(--surface-color);
    border-radius: var(--border-radius);
    box-shadow: var(--shadow);
    padding: 1.5rem;
    margin-bottom: 1rem;
    transition: box-shadow 0.3s ease;
}

.card:hover {
    box-shadow: var(--shadow-hover);
}

.card-header {
    border-bottom: 1px solid var(--border-color);
    padding-bottom: 1rem;
    margin-bottom: 1rem;
}

.card-title {
    margin: 0;
    font-size: 1.25rem;
    font-weight: 600;
}

/* Loading States */
.loading {
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 2rem;
    color: var(--text-secondary);
    font-style: italic;
}

.spinner {
    width: 20px;
    height: 20px;
    border: 2px solid var(--border-color);
    border-top: 2px solid var(--primary-color);
    border-radius: 50%;
    animation: spin 1s linear infinite;
    margin-right: 0.5rem;
}

@keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
}

/* Utility Classes */
.hidden {
    display: none !important;
}

.text-center {
    text-align: center;
}

.text-left {
    text-align: left;
}

.text-right {
    text-align: right;
}

.mb-1 { margin-bottom: 0.25rem; }
.mb-2 { margin-bottom: 0.5rem; }
.mb-3 { margin-bottom: 1rem; }
.mb-4 { margin-bottom: 1.5rem; }
.mb-5 { margin-bottom: 2rem; }

.mt-1 { margin-top: 0.25rem; }
.mt-2 { margin-top: 0.5rem; }
.mt-3 { margin-top: 1rem; }
.mt-4 { margin-top: 1.5rem; }
.mt-5 { margin-top: 2rem; }

.p-1 { padding: 0.25rem; }
.p-2 { padding: 0.5rem; }
.p-3 { padding: 1rem; }
.p-4 { padding: 1.5rem; }
.p-5 { padding: 2rem; }

/* Alerts and Messages */
.alert {
    padding: 0.75rem 1rem;
    border-radius: var(--border-radius);
    margin-bottom: 1rem;
    border: 1px solid transparent;
}

.alert-success {
    background-color: #d4edda;
    border-color: #c3e6cb;
    color: #155724;
}

.alert-warning {
    background-color: #fff3cd;
    border-color: #ffeaa7;
    color: #856404;
}

.alert-danger {
    background-color: #f8d7da;
    border-color: #f5c6cb;
    color: #721c24;
}

.alert-info {
    background-color: #d1ecf1;
    border-color: #bee5eb;
    color: #0c5460;
}

/* Icons */
.icon {
    font-size: 1rem;
    vertical-align: middle;
}

.icon-small {
    font-size: 0.75rem;
}

.icon-large {
    font-size: 1.5rem;
}

/* Scrollbars */
::-webkit-scrollbar {
    width: 8px;
    height: 8px;
}

::-webkit-scrollbar-track {
    background: var(--background-color);
    border-radius: 4px;
}

::-webkit-scrollbar-thumb {
    background: var(--border-color);
    border-radius: 4px;
    transition: background-color 0.3s ease;
}

::-webkit-scrollbar-thumb:hover {
    background: var(--text-secondary);
}
"""
        },

        {
            "path": "src\\main\\resources\\static\\css\\chat.css",
            "content": """/* Chat Interface CSS */

/* Main Chat App Layout */
.chat-app {
    display: flex;
    flex-direction: column;
    height: 100vh;
    background-color: var(--background-color);
}

/* Top Bar */
.top-bar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 1rem;
    background-color: var(--surface-color);
    border-bottom: 1px solid var(--border-color);
    box-shadow: var(--shadow);
    z-index: 100;
}

.search-container {
    display: flex;
    align-items: center;
    flex: 1;
    max-width: 600px;
}

.search-input {
    flex: 1;
    padding: 0.5rem 1rem;
    border: 2px solid var(--border-color);
    border-radius: 25px;
    font-size: 0.875rem;
    margin-right: 0.5rem;
    transition: all 0.3s ease;
}

.search-input:focus {
    border-color: var(--primary-color);
    box-shadow: 0 0 0 3px rgba(255, 69, 0, 0.1);
}

.filter-btn {
    padding: 0.5rem;
    background-color: var(--secondary-color);
    color: white;
    border: none;
    border-radius: 50%;
    cursor: pointer;
    transition: all 0.3s ease;
}

.filter-btn:hover {
    background-color: var(--secondary-hover);
    transform: scale(1.1);
}

.user-info {
    display: flex;
    align-items: center;
    gap: 1rem;
}

.username {
    font-weight: 600;
    color: var(--text-primary);
}

.settings-btn {
    padding: 0.5rem;
    background-color: transparent;
    border: 1px solid var(--border-color);
    border-radius: 50%;
    cursor: pointer;
    transition: all 0.3s ease;
}

.settings-btn:hover {
    background-color: var(--background-color);
    transform: scale(1.1);
}

/* Filter Panel */
.filter-panel {
    background-color: var(--surface-color);
    border-bottom: 1px solid var(--border-color);
    padding: 1rem;
    box-shadow: var(--shadow);
    z-index: 99;
}

.filter-controls {
    display: flex;
    align-items: center;
    gap: 1rem;
    flex-wrap: wrap;
}

.filter-controls input,
.filter-controls select {
    min-width: 150px;
}

/* Main Content Layout */
.main-content {
    display: flex;
    flex: 1;
    overflow: hidden;
}

/* Chat Panel (Right Side) */
.chat-panel {
    flex: 1;
    display: flex;
    flex-direction: column;
    background-color: var(--surface-color);
    border-left: 1px solid var(--border-color);
}

/* No Chat Selected State */
.no-chat-selected {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    flex: 1;
    text-align: center;
    color: var(--text-secondary);
    padding: 2rem;
}

.no-chat-selected h3 {
    color: var(--text-primary);
    margin-bottom: 0.5rem;
}

/* Active Chat Container */
.active-chat {
    display: flex;
    flex-direction: column;
    height: 100%;
}

/* Chat Header */
.chat-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 1rem;
    background-color: var(--surface-color);
    border-bottom: 1px solid var(--border-color);
    box-shadow: var(--shadow);
}

.chat-user-info {
    display: flex;
    align-items: center;
    gap: 0.75rem;
}

.avatar {
    width: 40px;
    height: 40px;
    border-radius: 50%;
    background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
    display: flex;
    align-items: center;
    justify-content: center;
    color: white;
    font-weight: bold;
    font-size: 1.1rem;
}

.avatar img {
    width: 100%;
    height: 100%;
    border-radius: 50%;
    object-fit: cover;
}

.user-details h4 {
    margin: 0;
    font-size: 1.1rem;
    color: var(--text-primary);
}

.online-status {
    font-size: 0.75rem;
    color: var(--success-color);
    font-weight: 500;
}

.chat-actions {
    display: flex;
    gap: 0.5rem;
}

.chat-actions .btn {
    padding: 0.5rem;
    border-radius: 50%;
    border: 1px solid var(--border-color);
    background-color: transparent;
    cursor: pointer;
    transition: all 0.3s ease;
}

.chat-actions .btn:hover {
    background-color: var(--background-color);
    transform: scale(1.1);
}

/* Messages Container */
.messages-container {
    flex: 1;
    overflow-y: auto;
    padding: 1rem;
    background: linear-gradient(to bottom, #f8f9fa 0%, #ffffff 100%);
}

/* Message Input Container */
.message-input-container {
    display: flex;
    align-items: center;
    padding: 1rem;
    background-color: var(--surface-color);
    border-top: 1px solid var(--border-color);
    gap: 0.5rem;
}

.message-input {
    flex: 1;
    padding: 0.75rem 1rem;
    border: 2px solid var(--border-color);
    border-radius: 25px;
    font-size: 0.875rem;
    resize: none;
    transition: all 0.3s ease;
    max-height: 120px;
    min-height: 44px;
}

.message-input:focus {
    border-color: var(--primary-color);
    box-shadow: 0 0 0 3px rgba(255, 69, 0, 0.1);
}

.send-btn {
    padding: 0.75rem;
    background-color: var(--primary-color);
    color: white;
    border: none;
    border-radius: 50%;
    cursor: pointer;
    transition: all 0.3s ease;
    width: 44px;
    height: 44px;
    display: flex;
    align-items: center;
    justify-content: center;
}

.send-btn:hover {
    background-color: var(--primary-hover);
    transform: scale(1.1);
}

.send-btn:disabled {
    background-color: var(--text-secondary);
    cursor: not-allowed;
    transform: none;
}

/* Message Bubbles */
.message-bubble {
    margin-bottom: 1rem;
    max-width: 70%;
    animation: messageSlide 0.3s ease-out;
}

@keyframes messageSlide {
    from {
        opacity: 0;
        transform: translateY(20px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

.own-message {
    margin-left: auto;
}

.other-message {
    margin-right: auto;
}

.message-content {
    background-color: var(--surface-color);
    padding: 0.75rem 1rem;
    border-radius: 18px;
    box-shadow: var(--shadow);
    position: relative;
    word-wrap: break-word;
}

.own-message .message-content {
    background-color: var(--primary-color);
    color: white;
}

.other-message .message-content {
    background-color: var(--background-color);
    color: var(--text-primary);
}

.message-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 0.5rem;
}

.sender-name {
    font-weight: 600;
    font-size: 0.75rem;
    color: var(--text-secondary);
}

.message-time {
    font-size: 0.7rem;
    color: var(--text-secondary);
    opacity: 0.8;
}

.own-message .message-time {
    color: rgba(255, 255, 255, 0.8);
}

.message-footer {
    display: flex;
    align-items: center;
    justify-content: flex-end;
    gap: 0.25rem;
    margin-top: 0.5rem;
}

.read-indicator,
.sent-indicator {
    font-size: 0.7rem;
    color: rgba(255, 255, 255, 0.8);
}

.read-indicator {
    color: var(--success-color);
}

/* Text Messages */
.text-message p {
    margin: 0;
    line-height: 1.4;
}

/* Image Messages */
.image-message {
    position: relative;
}

.message-image {
    max-width: 100%;
    max-height: 300px;
    border-radius: 12px;
    cursor: pointer;
    transition: transform 0.3s ease;
}

.message-image:hover {
    transform: scale(1.02);
}

.image-hidden {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    padding: 1rem;
    background-color: var(--background-color);
    border-radius: 12px;
    border: 2px dashed var(--border-color);
    color: var(--text-secondary);
}

.show-image-btn,
.hide-image-btn {
    padding: 0.25rem 0.5rem;
    background-color: var(--secondary-color);
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    font-size: 0.75rem;
    transition: background-color 0.3s ease;
}

.show-image-btn:hover,
.hide-image-btn:hover {
    background-color: var(--secondary-hover);
}

/* File Messages */
.file-message {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    padding: 0.5rem;
    background-color: var(--background-color);
    border-radius: 12px;
    border: 1px solid var(--border-color);
}

.file-info {
    flex: 1;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

.file-details {
    flex: 1;
}

.file-name {
    font-weight: 600;
    color: var(--text-primary);
    display: block;
    font-size: 0.875rem;
}

.file-size {
    font-size: 0.75rem;
    color: var(--text-secondary);
}

.download-btn {
    padding: 0.5rem;
    background-color: var(--secondary-color);
    color: white;
    border: none;
    border-radius: 50%;
    cursor: pointer;
    transition: all 0.3s ease;
}

.download-btn:hover {
    background-color: var(--secondary-hover);
    transform: scale(1.1);
}

/* System Messages */
.system-message {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 0.5rem;
    padding: 0.5rem 1rem;
    background-color: var(--info-color);
    color: white;
    border-radius: 12px;
    font-size: 0.875rem;
    font-style: italic;
}

/* Message Actions */
.message-actions {
    position: absolute;
    top: -10px;
    right: 10px;
    display: flex;
    gap: 0.25rem;
    opacity: 0;
    transition: opacity 0.3s ease;
}

.message-bubble:hover .message-actions {
    opacity: 1;
}

.message-actions button {
    padding: 0.25rem;
    background-color: var(--surface-color);
    border: 1px solid var(--border-color);
    border-radius: 4px;
    cursor: pointer;
    font-size: 0.75rem;
    transition: all 0.3s ease;
    box-shadow: var(--shadow);
}

.message-actions button:hover {
    background-color: var(--background-color);
    transform: scale(1.1);
}

/* Typing Indicator */
.typing-indicator {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.5rem 1rem;
    background-color: var(--background-color);
    border-radius: 18px;
    margin-bottom: 1rem;
    max-width: 200px;
    animation: fadeIn 0.3s ease-out;
}

@keyframes fadeIn {
    from {
        opacity: 0;
    }
    to {
        opacity: 1;
    }
}

.typing-avatar {
    width: 24px;
    height: 24px;
    border-radius: 50%;
    overflow: hidden;
}

.typing-avatar img {
    width: 100%;
    height: 100%;
    object-fit: cover;
}

.typing-content {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    font-size: 0.875rem;
    color: var(--text-secondary);
}

.typing-dots {
    display: flex;
    gap: 2px;
}

.typing-dots span {
    width: 4px;
    height: 4px;
    border-radius: 50%;
    background-color: var(--text-secondary);
    animation: typingDots 1.4s ease-in-out infinite;
}

.typing-dots span:nth-child(1) {
    animation-delay: 0s;
}

.typing-dots span:nth-child(2) {
    animation-delay: 0.2s;
}

.typing-dots span:nth-child(3) {
    animation-delay: 0.4s;
}

@keyframes typingDots {
    0%, 60%, 100% {
        transform: scale(0.8);
        opacity: 0.5;
    }
    30% {
        transform: scale(1.2);
        opacity: 1;
    }
}

/* Date Separator */
.date-separator {
    text-align: center;
    margin: 1rem 0;
    position: relative;
}

.date-separator::before {
    content: '';
    position: absolute;
    top: 50%;
    left: 0;
    right: 0;
    height: 1px;
    background-color: var(--border-color);
    z-index: 1;
}

.date-separator span {
    background-color: var(--surface-color);
    padding: 0.25rem 0.5rem;
    font-size: 0.75rem;
    color: var(--text-secondary);
    border-radius: 12px;
    position: relative;
    z-index: 2;
}
"""
        },

        {
            "path": "src\\main\\resources\\static\\css\\sidebar.css",
            "content": """/* Sidebar CSS */

/* Main Sidebar */
.chat-sidebar {
    width: 300px;
    background-color: var(--surface-color);
    border-right: 1px solid var(--border-color);
    display: flex;
    flex-direction: column;
    height: 100%;
    overflow: hidden;
}

/* Sidebar Header */
.sidebar-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 1rem;
    border-bottom: 1px solid var(--border-color);
    background-color: var(--surface-color);
}

.sidebar-header h3 {
    margin: 0;
    font-size: 1.25rem;
    color: var(--text-primary);
}

.sidebar-actions {
    display: flex;
    gap: 0.5rem;
}

.bulk-select-btn,
.new-chat-btn {
    padding: 0.5rem;
    border: 1px solid var(--border-color);
    background-color: transparent;
    border-radius: var(--border-radius);
    cursor: pointer;
    transition: all 0.3s ease;
    font-size: 0.75rem;
}

.bulk-select-btn:hover,
.new-chat-btn:hover {
    background-color: var(--background-color);
    transform: translateY(-1px);
}

.bulk-select-btn.active {
    background-color: var(--primary-color);
    color: white;
    border-color: var(--primary-color);
}

.new-chat-btn {
    width: 32px;
    height: 32px;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 50%;
    background-color: var(--primary-color);
    color: white;
    border: none;
}

.new-chat-btn:hover {
    background-color: var(--primary-hover);
    transform: scale(1.1);
}

/* Search Container */
.search-container {
    padding: 1rem;
    border-bottom: 1px solid var(--border-color);
}

.search-input {
    width: 100%;
    padding: 0.5rem 0.75rem;
    border: 2px solid var(--border-color);
    border-radius: 20px;
    font-size: 0.875rem;
    transition: all 0.3s ease;
}

.search-input:focus {
    border-color: var(--primary-color);
    box-shadow: 0 0 0 3px rgba(255, 69, 0, 0.1);
}

.search-btn {
    position: absolute;
    right: 1.5rem;
    top: 50%;
    transform: translateY(-50%);
    background: none;
    border: none;
    color: var(--text-secondary);
    cursor: pointer;
    padding: 0.25rem;
}

/* Filter Options */
.filter-options {
    display: flex;
    padding: 0.5rem 1rem;
    gap: 0.5rem;
    border-bottom: 1px solid var(--border-color);
    background-color: var(--background-color);
}

.filter-btn {
    padding: 0.375rem 0.75rem;
    border: 1px solid var(--border-color);
    background-color: var(--surface-color);
    color: var(--text-secondary);
    border-radius: 20px;
    cursor: pointer;
    font-size: 0.75rem;
    font-weight: 500;
    transition: all 0.3s ease;
    white-space: nowrap;
}

.filter-btn:hover {
    background-color: var(--background-color);
    border-color: var(--text-secondary);
}

.filter-btn.active {
    background-color: var(--primary-color);
    color: white;
    border-color: var(--primary-color);
}

/* Chat List */
.chat-list {
    flex: 1;
    overflow-y: auto;
    padding: 0.5rem 0;
}

.chat-list:empty::before {
    content: "No chats available";
    display: block;
    text-align: center;
    color: var(--text-secondary);
    padding: 2rem;
    font-style: italic;
}

/* Chat Item */
.chat-item {
    display: flex;
    align-items: center;
    padding: 0.75rem 1rem;
    cursor: pointer;
    transition: all 0.3s ease;
    border-bottom: 1px solid rgba(237, 239, 241, 0.5);
    position: relative;
}

.chat-item:hover {
    background-color: var(--background-color);
}

.chat-item.active {
    background-color: var(--primary-color);
    color: white;
}

.chat-item.active .chat-username,
.chat-item.active .last-message,
.chat-item.active .chat-time {
    color: white;
}

.chat-item.selected {
    background-color: rgba(255, 69, 0, 0.1);
    border-left: 4px solid var(--primary-color);
}

/* Chat Avatar */
.chat-avatar {
    position: relative;
    margin-right: 0.75rem;
    flex-shrink: 0;
}

.avatar-img {
    width: 48px;
    height: 48px;
    border-radius: 50%;
    object-fit: cover;
    background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
}

.unread-indicator {
    position: absolute;
    top: 0;
    right: 0;
    width: 12px;
    height: 12px;
    background-color: var(--success-color);
    border-radius: 50%;
    border: 2px solid var(--surface-color);
}

/* Chat Content */
.chat-content {
    flex: 1;
    min-width: 0;
    overflow: hidden;
}

.chat-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 0.25rem;
}

.chat-username {
    font-weight: 600;
    font-size: 0.875rem;
    color: var(--text-primary);
}

.chat-time {
    font-size: 0.75rem;
    color: var(--text-secondary);
    flex-shrink: 0;
}

.chat-preview {
    display: flex;
    align-items: center;
    justify-content: space-between;
}

.last-message {
    font-size: 0.8rem;
    color: var(--text-secondary);
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
    flex: 1;
    margin-right: 0.5rem;
}

.chat-indicators {
    display: flex;
    align-items: center;
    gap: 0.25rem;
    flex-shrink: 0;
}

.pinned-indicator {
    font-size: 0.75rem;
    color: var(--warning-color);
}

.unread-count {
    background-color: var(--danger-color);
    color: white;
    font-size: 0.7rem;
    font-weight: bold;
    padding: 0.125rem 0.375rem;
    border-radius: 10px;
    min-width: 18px;
    text-align: center;
    line-height: 1.2;
}

.chat-item.active .unread-count {
    background-color: rgba(255, 255, 255, 0.9);
    color: var(--primary-color);
}

/* Chat Actions */
.chat-actions {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    opacity: 0;
    transition: opacity 0.3s ease;
    margin-left: 0.5rem;
}

.chat-item:hover .chat-actions {
    opacity: 1;
}

.pin-btn {
    padding: 0.25rem;
    background: none;
    border: 1px solid var(--border-color);
    border-radius: 4px;
    cursor: pointer;
    color: var(--text-secondary);
    transition: all 0.3s ease;
}

.pin-btn:hover {
    background-color: var(--background-color);
    color: var(--warning-color);
    transform: scale(1.1);
}

.chat-checkbox {
    opacity: 0;
    transition: opacity 0.3s ease;
}

.bulk-mode .chat-checkbox {
    opacity: 1;
}

.chat-select-checkbox {
    width: 16px;
    height: 16px;
    cursor: pointer;
}

/* Bulk Actions */
.bulk-actions {
    padding: 1rem;
    border-top: 1px solid var(--border-color);
    background-color: var(--background-color);
    display: flex;
    gap: 0.5rem;
    flex-wrap: wrap;
}

.bulk-actions .btn {
    flex: 1;
    padding: 0.5rem 0.75rem;
    font-size: 0.75rem;
    white-space: nowrap;
}

/* Loading State */
.chat-list .loading {
    padding: 2rem 1rem;
    text-align: center;
    color: var(--text-secondary);
}

/* Empty State */
.empty-state {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 2rem 1rem;
    text-align: center;
    color: var(--text-secondary);
}

.empty-state h4 {
    margin-bottom: 0.5rem;
    color: var(--text-primary);
}

.empty-state p {
    margin-bottom: 1rem;
    font-size: 0.875rem;
}

/* Status Indicators */
.online-status {
    width: 8px;
    height: 8px;
    background-color: var(--success-color);
    border-radius: 50%;
    position: absolute;
    bottom: 2px;
    right: 2px;
    border: 2px solid var(--surface-color);
}

.offline-status {
    width: 8px;
    height: 8px;
    background-color: var(--text-secondary);
    border-radius: 50%;
    position: absolute;
    bottom: 2px;
    right: 2px;
    border: 2px solid var(--surface-color);
}

/* Scroll to bottom button */
.scroll-to-bottom {
    position: fixed;
    bottom: 100px;
    right: 20px;
    width: 40px;
    height: 40px;
    background-color: var(--primary-color);
    color: white;
    border: none;
    border-radius: 50%;
    cursor: pointer;
    box-shadow: var(--shadow-hover);
    transition: all 0.3s ease;
    z-index: 100;
}

.scroll-to-bottom:hover {
    background-color: var(--primary-hover);
    transform: scale(1.1);
}

.scroll-to-bottom.hidden {
    opacity: 0;
    pointer-events: none;
}
"""
        },

        {
            "path": "src\\main\\resources\\static\\css\\modal.css",
            "content": """/* Modal CSS */

/* Modal Overlay */
.modal-overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0, 0, 0, 0.5);
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 1000;
    backdrop-filter: blur(2px);
    animation: modalOverlayFadeIn 0.3s ease-out;
}

@keyframes modalOverlayFadeIn {
    from {
        opacity: 0;
    }
    to {
        opacity: 1;
    }
}

/* Modal Container */
.modal {
    background-color: var(--surface-color);
    border-radius: var(--border-radius);
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
    max-width: 90vw;
    max-height: 90vh;
    overflow-y: auto;
    position: relative;
    animation: modalSlideIn 0.3s ease-out;
}

@keyframes modalSlideIn {
    from {
        opacity: 0;
        transform: translateY(-50px) scale(0.9);
    }
    to {
        opacity: 1;
        transform: translateY(0) scale(1);
    }
}

.modal-small {
    width: 400px;
}

.modal-medium {
    width: 600px;
}

.modal-large {
    width: 800px;
}

.modal-fullscreen {
    width: 95vw;
    height: 95vh;
}

/* Modal Header */
.modal-header {
    display: flex;
    align-items: center;
    justify-content: between;
    padding: 1.5rem;
    border-bottom: 1px solid var(--border-color);
}

.modal-title {
    flex: 1;
    margin: 0;
    font-size: 1.25rem;
    font-weight: 600;
    color: var(--text-primary);
}

.modal-close {
    background: none;
    border: none;
    font-size: 1.5rem;
    cursor: pointer;
    color: var(--text-secondary);
    padding: 0.25rem;
    border-radius: 4px;
    transition: all 0.3s ease;
    margin-left: 1rem;
}

.modal-close:hover {
    background-color: var(--background-color);
    color: var(--text-primary);
    transform: scale(1.1);
}

/* Modal Body */
.modal-body {
    padding: 1.5rem;
    max-height: 60vh;
    overflow-y: auto;
}

/* Modal Footer */
.modal-footer {
    display: flex;
    align-items: center;
    justify-content: flex-end;
    gap: 1rem;
    padding: 1.5rem;
    border-top: 1px solid var(--border-color);
    background-color: var(--background-color);
}

/* Specific Modal Types */

/* New Chat Modal */
.new-chat-modal .modal-body {
    padding: 2rem;
}

.user-search-container {
    position: relative;
    margin-bottom: 1.5rem;
}

.user-search-input {
    width: 100%;
    padding: 0.75rem 1rem;
    border: 2px solid var(--border-color);
    border-radius: var(--border-radius);
    font-size: 1rem;
}

.user-search-input:focus {
    border-color: var(--primary-color);
    box-shadow: 0 0 0 3px rgba(255, 69, 0, 0.1);
}

.user-suggestions {
    position: absolute;
    top: 100%;
    left: 0;
    right: 0;
    background-color: var(--surface-color);
    border: 1px solid var(--border-color);
    border-radius: var(--border-radius);
    box-shadow: var(--shadow);
    max-height: 200px;
    overflow-y: auto;
    z-index: 10;
}

.user-suggestion {
    display: flex;
    align-items: center;
    padding: 0.75rem 1rem;
    cursor: pointer;
    transition: background-color 0.3s ease;
    gap: 0.75rem;
}

.user-suggestion:hover {
    background-color: var(--background-color);
}

.user-suggestion .avatar-img {
    width: 32px;
    height: 32px;
    border-radius: 50%;
}

.user-suggestion-info h5 {
    margin: 0;
    font-size: 0.875rem;
    color: var(--text-primary);
}

.user-suggestion-info p {
    margin: 0;
    font-size: 0.75rem;
    color: var(--text-secondary);
}

/* Settings Modal */
.settings-modal .modal-body {
    padding: 0;
}

.settings-nav {
    display: flex;
    border-bottom: 1px solid var(--border-color);
}

.settings-nav-item {
    padding: 1rem 1.5rem;
    cursor: pointer;
    border-bottom: 2px solid transparent;
    transition: all 0.3s ease;
    font-weight: 500;
}

.settings-nav-item:hover {
    background-color: var(--background-color);
}

.settings-nav-item.active {
    border-bottom-color: var(--primary-color);
    color: var(--primary-color);
}

.settings-content {
    padding: 2rem;
}

.settings-section {
    margin-bottom: 2rem;
}

.settings-section h4 {
    margin-bottom: 1rem;
    color: var(--text-primary);
}

.setting-item {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 1rem 0;
    border-bottom: 1px solid var(--border-color);
}

.setting-item:last-child {
    border-bottom: none;
}

.setting-label {
    flex: 1;
}

.setting-label h5 {
    margin: 0 0 0.25rem 0;
    font-size: 1rem;
    color: var(--text-primary);
}

.setting-label p {
    margin: 0;
    font-size: 0.875rem;
    color: var(--text-secondary);
}

.setting-control {
    flex-shrink: 0;
}

/* Toggle Switch */
.toggle-switch {
    position: relative;
    width: 50px;
    height: 24px;
    background-color: var(--border-color);
    border-radius: 12px;
    cursor: pointer;
    transition: background-color 0.3s ease;
}

.toggle-switch.active {
    background-color: var(--primary-color);
}

.toggle-switch::after {
    content: '';
    position: absolute;
    top: 2px;
    left: 2px;
    width: 20px;
    height: 20px;
    background-color: white;
    border-radius: 50%;
    transition: transform 0.3s ease;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
}

.toggle-switch.active::after {
    transform: translateX(26px);
}

/* Image Viewer Modal */
.image-viewer-modal {
    background-color: rgba(0, 0, 0, 0.9);
    padding: 2rem;
    display: flex;
    align-items: center;
    justify-content: center;
}

.image-viewer-content {
    position: relative;
    max-width: 90vw;
    max-height: 90vh;
}

.image-viewer-content img {
    max-width: 100%;
    max-height: 100%;
    object-fit: contain;
    border-radius: var(--border-radius);
}

.image-viewer-controls {
    position: absolute;
    top: 10px;
    right: 10px;
    display: flex;
    gap: 0.5rem;
}

.image-viewer-controls button {
    background-color: rgba(0, 0, 0, 0.7);
    color: white;
    border: none;
    padding: 0.5rem;
    border-radius: 4px;
    cursor: pointer;
    transition: background-color 0.3s ease;
}

.image-viewer-controls button:hover {
    background-color: rgba(0, 0, 0, 0.9);
}

/* Export Options Modal */
.export-modal .export-options {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 1rem;
    margin-bottom: 2rem;
}

.export-option {
    padding: 1rem;
    border: 2px solid var(--border-color);
    border-radius: var(--border-radius);
    cursor: pointer;
    transition: all 0.3s ease;
    text-align: center;
}

.export-option:hover {
    border-color: var(--primary-color);
    transform: translateY(-2px);
}

.export-option.selected {
    border-color: var(--primary-color);
    background-color: rgba(255, 69, 0, 0.1);
}

.export-option h5 {
    margin: 0 0 0.5rem 0;
    color: var(--text-primary);
}

.export-option p {
    margin: 0;
    font-size: 0.875rem;
    color: var(--text-secondary);
}

/* Block Users Modal */
.blocked-users-list {
    max-height: 400px;
    overflow-y: auto;
}

.blocked-user-item {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 1rem;
    border-bottom: 1px solid var(--border-color);
}

.blocked-user-item:last-child {
    border-bottom: none;
}

.blocked-user-info {
    display: flex;
    align-items: center;
    gap: 0.75rem;
}

.blocked-user-info .avatar-img {
    width: 40px;
    height: 40px;
    border-radius: 50%;
}

.blocked-user-details h5 {
    margin: 0;
    color: var(--text-primary);
}

.blocked-user-details p {
    margin: 0;
    font-size: 0.875rem;
    color: var(--text-secondary);
}

/* Progress Modal */
.progress-modal .progress-container {
    margin: 2rem 0;
}

.progress-bar {
    width: 100%;
    height: 8px;
    background-color: var(--border-color);
    border-radius: 4px;
    overflow: hidden;
}

.progress-fill {
    height: 100%;
    background-color: var(--primary-color);
    transition: width 0.3s ease;
    border-radius: 4px;
}

.progress-text {
    text-align: center;
    margin-top: 1rem;
    color: var(--text-secondary);
    font-size: 0.875rem;
}

/* Responsive Design */
@media (max-width: 768px) {
    .modal {
        width: 95vw !important;
        margin: 1rem;
        max-height: 95vh;
    }
    
    .modal-header,
    .modal-body,
    .modal-footer {
        padding: 1rem;
    }
    
    .settings-nav {
        overflow-x: auto;
        white-space: nowrap;
    }
    
    .export-options {
        grid-template-columns: 1fr;
    }
}
"""
        },

        {
            "path": "src\\main\\resources\\static\\css\\animations.css",
            "content": """/* Animations CSS */

/* Fade Animations */
@keyframes fadeIn {
    from {
        opacity: 0;
    }
    to {
        opacity: 1;
    }
}

@keyframes fadeOut {
    from {
        opacity: 1;
    }
    to {
        opacity: 0;
    }
}

@keyframes fadeInUp {
    from {
        opacity: 0;
        transform: translateY(20px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

@keyframes fadeInDown {
    from {
        opacity: 0;
        transform: translateY(-20px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

@keyframes fadeInLeft {
    from {
        opacity: 0;
        transform: translateX(-20px);
    }
    to {
        opacity: 1;
        transform: translateX(0);
    }
}

@keyframes fadeInRight {
    from {
        opacity: 0;
        transform: translateX(20px);
    }
    to {
        opacity: 1;
        transform: translateX(0);
    }
}

/* Scale Animations */
@keyframes scaleIn {
    from {
        opacity: 0;
        transform: scale(0.9);
    }
    to {
        opacity: 1;
        transform: scale(1);
    }
}

@keyframes scaleOut {
    from {
        opacity: 1;
        transform: scale(1);
    }
    to {
        opacity: 0;
        transform: scale(0.9);
    }
}

/* Slide Animations */
@keyframes slideInLeft {
    from {
        transform: translateX(-100%);
    }
    to {
        transform: translateX(0);
    }
}

@keyframes slideInRight {
    from {
        transform: translateX(100%);
    }
    to {
        transform: translateX(0);
    }
}

@keyframes slideInUp {
    from {
        transform: translateY(100%);
    }
    to {
        transform: translateY(0);
    }
}

@keyframes slideInDown {
    from {
        transform: translateY(-100%);
    }
    to {
        transform: translateY(0);
    }
}

/* Bounce Animations */
@keyframes bounce {
    0%, 20%, 53%, 80%, 100% {
        transform: translateY(0);
    }
    40%, 43% {
        transform: translateY(-10px);
    }
    70% {
        transform: translateY(-5px);
    }
    90% {
        transform: translateY(-2px);
    }
}

@keyframes bounceIn {
    0% {
        opacity: 0;
        transform: scale(0.3);
    }
    50% {
        opacity: 1;
        transform: scale(1.05);
    }
    70% {
        transform: scale(0.9);
    }
    100% {
        opacity: 1;
        transform: scale(1);
    }
}

/* Pulse Animation */
@keyframes pulse {
    0% {
        transform: scale(1);
    }
    50% {
        transform: scale(1.05);
    }
    100% {
        transform: scale(1);
    }
}

/* Shake Animation */
@keyframes shake {
    0%, 100% {
        transform: translateX(0);
    }
    10%, 30%, 50%, 70%, 90% {
        transform: translateX(-5px);
    }
    20%, 40%, 60%, 80% {
        transform: translateX(5px);
    }
}

/* Rotate Animations */
@keyframes rotate {
    from {
        transform: rotate(0deg);
    }
    to {
        transform: rotate(360deg);
    }
}

@keyframes rotateIn {
    from {
        opacity: 0;
        transform: rotate(-180deg) scale(0.5);
    }
    to {
        opacity: 1;
        transform: rotate(0deg) scale(1);
    }
}

/* Glow Animation */
@keyframes glow {
    0%, 100% {
        box-shadow: 0 0 5px rgba(255, 69, 0, 0.3);
    }
    50% {
        box-shadow: 0 0 20px rgba(255, 69, 0, 0.6);
    }
}

/* Typing Animation */
@keyframes typing {
    0%, 60%, 100% {
        transform: scale(0.8);
        opacity: 0.5;
    }
    30% {
        transform: scale(1.2);
        opacity: 1;
    }
}

/* Progress Bar Animation */
@keyframes progressBar {
    from {
        width: 0%;
    }
    to {
        width: var(--progress-width, 100%);
    }
}

/* Notification Slide */
@keyframes notificationSlide {
    from {
        transform: translateX(100%);
        opacity: 0;
    }
    to {
        transform: translateX(0);
        opacity: 1;
    }
}

/* Chat Message Animations */
@keyframes messageAppear {
    from {
        opacity: 0;
        transform: translateY(20px) scale(0.95);
    }
    to {
        opacity: 1;
        transform: translateY(0) scale(1);
    }
}

@keyframes messageHighlight {
    0% {
        background-color: transparent;
    }
    50% {
        background-color: rgba(255, 69, 0, 0.1);
    }
    100% {
        background-color: transparent;
    }
}

/* Button Hover Animations */
@keyframes buttonPop {
    0% {
        transform: scale(1);
    }
    50% {
        transform: scale(1.1);
    }
    100% {
        transform: scale(1);
    }
}

/* Loading Spinner */
@keyframes spin {
    from {
        transform: rotate(0deg);
    }
    to {
        transform: rotate(360deg);
    }
}

/* Ripple Effect */
@keyframes ripple {
    0% {
        transform: scale(0);
        opacity: 0.7;
    }
    100% {
        transform: scale(4);
        opacity: 0;
    }
}

/* Animation Classes */
.fade-in {
    animation: fadeIn 0.3s ease-out;
}

.fade-out {
    animation: fadeOut 0.3s ease-out;
}

.fade-in-up {
    animation: fadeInUp 0.4s ease-out;
}

.fade-in-down {
    animation: fadeInDown 0.4s ease-out;
}

.fade-in-left {
    animation: fadeInLeft 0.4s ease-out;
}

.fade-in-right {
    animation: fadeInRight 0.4s ease-out;
}

.scale-in {
    animation: scaleIn 0.3s ease-out;
}

.scale-out {
    animation: scaleOut 0.3s ease-out;
}

.slide-in-left {
    animation: slideInLeft 0.4s ease-out;
}

.slide-in-right {
    animation: slideInRight 0.4s ease-out;
}

.slide-in-up {
    animation: slideInUp 0.4s ease-out;
}

.slide-in-down {
    animation: slideInDown 0.4s ease-out;
}

.bounce {
    animation: bounce 1s ease-in-out;
}

.bounce-in {
    animation: bounceIn 0.6s ease-out;
}

.pulse {
    animation: pulse 2s ease-in-out infinite;
}

.shake {
    animation: shake 0.6s ease-in-out;
}

.rotate {
    animation: rotate 2s linear infinite;
}

.rotate-in {
    animation: rotateIn 0.6s ease-out;
}

.glow {
    animation: glow 2s ease-in-out infinite;
}

.message-appear {
    animation: messageAppear 0.4s ease-out;
}

.message-highlight {
    animation: messageHighlight 1s ease-out;
}

.notification-slide {
    animation: notificationSlide 0.4s ease-out;
}

/* Transition Classes */
.transition-all {
    transition: all 0.3s ease;
}

.transition-fast {
    transition: all 0.15s ease;
}

.transition-slow {
    transition: all 0.6s ease;
}

.transition-colors {
    transition: color 0.3s ease, background-color 0.3s ease, border-color 0.3s ease;
}

.transition-transform {
    transition: transform 0.3s ease;
}

.transition-opacity {
    transition: opacity 0.3s ease;
}

/* Hover Effects */
.hover-lift:hover {
    transform: translateY(-2px);
    box-shadow: var(--shadow-hover);
}

.hover-grow:hover {
    transform: scale(1.05);
}

.hover-shrink:hover {
    transform: scale(0.95);
}

.hover-rotate:hover {
    transform: rotate(5deg);
}

.hover-glow:hover {
    box-shadow: 0 0 15px rgba(255, 69, 0, 0.4);
}

.hover-fade:hover {
    opacity: 0.8;
}

/* Loading States */
.skeleton {
    background: linear-gradient(90deg, #f0f0f0 25%, #e0e0e0 50%, #f0f0f0 75%);
    background-size: 200% 100%;
    animation: skeleton-loading 1.5s infinite;
}

@keyframes skeleton-loading {
    0% {
        background-position: 200% 0;
    }
    100% {
        background-position: -200% 0;
    }
}

/* Stagger Animation Delays */
.stagger-1 { animation-delay: 0.1s; }
.stagger-2 { animation-delay: 0.2s; }
.stagger-3 { animation-delay: 0.3s; }
.stagger-4 { animation-delay: 0.4s; }
.stagger-5 { animation-delay: 0.5s; }

/* Performance Optimizations */
.will-change-transform {
    will-change: transform;
}

.will-change-opacity {
    will-change: opacity;
}

.will-change-auto {
    will-change: auto;
}

/* Reduced Motion Support */
@media (prefers-reduced-motion: reduce) {
    *,
    *::before,
    *::after {
        animation-duration: 0.01ms !important;
        animation-iteration-count: 1 !important;
        transition-duration: 0.01ms !important;
    }
    
    .pulse,
    .bounce,
    .rotate {
        animation: none;
    }
}
"""
        },

        {
            "path": "src\\main\\resources\\static\\css\\responsive.css",
            "content": """/* Responsive CSS */

/* Breakpoints */
/* xs: 0-575px (phones) */
/* sm: 576-767px (large phones) */
/* md: 768-991px (tablets) */
/* lg: 992-1199px (desktops) */
/* xl: 1200px+ (large desktops) */

/* Extra Large Screens (1200px and up) */
@media (min-width: 1200px) {
    .container {
        max-width: 1200px;
    }
    
    .chat-sidebar {
        width: 350px;
    }
    
    .message-bubble {
        max-width: 65%;
    }
}

/* Large Screens (992px to 1199px) */
@media (min-width: 992px) and (max-width: 1199px) {
    .container {
        max-width: 960px;
    }
    
    .chat-sidebar {
        width: 300px;
    }
    
    .message-bubble {
        max-width: 70%;
    }
    
    .filter-controls {
        gap: 0.5rem;
    }
}

/* Medium Screens (768px to 991px) - Tablets */
@media (min-width: 768px) and (max-width: 991px) {
    .container {
        max-width: 720px;
    }
    
    .main-content {
        flex-direction: column;
    }
    
    .chat-sidebar {
        width: 100%;
        height: 300px;
        border-right: none;
        border-bottom: 1px solid var(--border-color);
    }
    
    .chat-panel {
        border-left: none;
        flex: 1;
    }
    
    .top-bar {
        flex-direction: column;
        gap: 1rem;
        padding: 1rem;
    }
    
    .search-container {
        max-width: none;
        width: 100%;
    }
    
    .filter-controls {
        flex-direction: column;
        gap: 0.5rem;
    }
    
    .filter-controls input,
    .filter-controls select {
        width: 100%;
        min-width: auto;
    }
    
    .message-bubble {
        max-width: 80%;
    }
    
    .chat-actions {
        flex-wrap: wrap;
    }
    
    .bulk-actions {
        flex-direction: column;
    }
    
    .bulk-actions .btn {
        width: 100%;
        margin-bottom: 0.5rem;
    }
}

/* Small Screens (576px to 767px) - Large Phones */
@media (min-width: 576px) and (max-width: 767px) {
    .container {
        padding: 0 0.5rem;
    }
    
    .main-content {
        flex-direction: column;
    }
    
    .chat-sidebar {
        width: 100%;
        height: 250px;
    }
    
    .top-bar {
        padding: 0.75rem;
        flex-direction: column;
        gap: 0.75rem;
    }
    
    .search-input {
        font-size: 16px; /* Prevent zoom on iOS */
    }
    
    .filter-options {
        justify-content: center;
        overflow-x: auto;
        white-space: nowrap;
        padding: 0.5rem;
    }
    
    .filter-btn {
        flex-shrink: 0;
    }
    
    .message-input-container {
        padding: 0.75rem;
        gap: 0.75rem;
    }
    
    .message-input {
        font-size: 16px; /* Prevent zoom on iOS */
        padding: 0.75rem;
    }
    
    .message-bubble {
        max-width: 85%;
    }
    
    .chat-header {
        padding: 0.75rem;
    }
    
    .chat-actions .btn {
        padding: 0.375rem;
        font-size: 0.75rem;
    }
    
    .modal {
        width: 95vw !important;
        margin: 1rem !important;
    }
    
    .modal-header,
    .modal-body,
    .modal-footer {
        padding: 1rem;
    }
    
    .settings-nav {
        overflow-x: auto;
    }
    
    .settings-nav-item {
        white-space: nowrap;
        flex-shrink: 0;
    }
}

/* Extra Small Screens (up to 575px) - Phones */
@media (max-width: 575px) {
    .container {
        padding: 0;
    }
    
    .chat-app {
        height: 100vh;
        height: -webkit-fill-available; /* iOS Safari fix */
    }
    
    .main-content {
        flex-direction: column;
        height: 100%;
    }
    
    .chat-sidebar {
        width: 100%;
        height: 200px;
        min-height: 200px;
    }
    
    .chat-panel {
        flex: 1;
        display: flex;
        flex-direction: column;
        min-height: 0;
    }
    
    .top-bar {
        padding: 0.5rem;
        flex-direction: column;
        gap: 0.5rem;
    }
    
    .user-info {
        justify-content: center;
        width: 100%;
    }
    
    .search-container {
        width: 100%;
    }
    
    .search-input {
        font-size: 16px; /* Prevent zoom on iOS */
        padding: 0.625rem 0.75rem;
    }
    
    /* Hide sidebar when chat is active on mobile */
    .mobile-chat-active .chat-sidebar {
        display: none;
    }
    
    .mobile-chat-active .chat-panel {
        height: 100vh;
        height: -webkit-fill-available;
    }
    
    /* Mobile Chat Header */
    .chat-header {
        padding: 0.75rem;
        position: relative;
    }
    
    .mobile-back-btn {
        display: block;
        position: absolute;
        left: 0.75rem;
        top: 50%;
        transform: translateY(-50%);
        background: none;
        border: none;
        font-size: 1.25rem;
        cursor: pointer;
        color: var(--text-primary);
        padding: 0.25rem;
    }
    
    .chat-user-info {
        margin-left: 2rem; /* Space for back button */
    }
    
    /* Mobile Message Input */
    .message-input-container {
        padding: 0.5rem;
        gap: 0.5rem;
        background-color: var(--surface-color);
        border-top: 1px solid var(--border-color);
    }
    
    .message-input {
        font-size: 16px; /* Prevent zoom on iOS */
        padding: 0.625rem 0.875rem;
        border-radius: 20px;
    }
    
    .send-btn {
        width: 40px;
        height: 40px;
        padding: 0.5rem;
    }
    
    /* Mobile Messages */
    .messages-container {
        padding: 0.75rem;
        -webkit-overflow-scrolling: touch; /* Smooth scrolling on iOS */
    }
    
    .message-bubble {
        max-width: 90%;
        margin-bottom: 0.75rem;
    }
    
    .message-content {
        padding: 0.625rem 0.875rem;
        font-size: 0.875rem;
        line-height: 1.4;
    }
    
    .message-time {
        font-size: 0.7rem;
    }
    
    .message-actions {
        position: static;
        opacity: 1;
        margin-top: 0.5rem;
        justify-content: center;
    }
    
    .message-actions button {
        padding: 0.375rem 0.5rem;
        font-size: 0.7rem;
    }
    
    /* Mobile Chat List */
    .chat-item {
        padding: 0.875rem;
    }
    
    .chat-avatar .avatar-img {
        width: 44px;
        height: 44px;
    }
    
    .chat-content {
        margin-left: 0.625rem;
    }
    
    .chat-username {
        font-size: 1rem;
    }
    
    .last-message {
        font-size: 0.875rem;
    }
    
    .chat-time {
        font-size: 0.75rem;
    }
    
    /* Mobile Modals */
    .modal {
        width: 100vw !important;
        height: 100vh !important;
        max-width: 100vw !important;
        max-height: 100vh !important;
        margin: 0 !important;
        border-radius: 0 !important;
    }
    
    .modal-header {
        padding: 1rem 0.75rem;
        border-bottom: 1px solid var(--border-color);
        position: sticky;
        top: 0;
        background-color: var(--surface-color);
        z-index: 10;
    }
    
    .modal-body {
        padding: 1rem 0.75rem;
        height: calc(100vh - 120px);
        overflow-y: auto;
    }
    
    .modal-footer {
        padding: 1rem 0.75rem;
        position: sticky;
        bottom: 0;
        background-color: var(--surface-color);
        border-top: 1px solid var(--border-color);
    }
    
    /* Mobile Filter Panel */
    .filter-panel {
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        z-index: 1000;
        background-color: var(--surface-color);
        border-radius: 0;
    }
    
    .filter-controls {
        flex-direction: column;
        padding: 1rem 0.75rem;
    }
    
    .filter-controls input,
    .filter-controls select,
    .filter-controls button {
        width: 100%;
        margin-bottom: 0.75rem;
        font-size: 16px;
    }
    
    /* Mobile Bulk Actions */
    .bulk-actions {
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        background-color: var(--surface-color);
        border-top: 2px solid var(--border-color);
        box-shadow: 0 -4px 8px rgba(0, 0, 0, 0.1);
        z-index: 100;
        padding: 0.75rem;
    }
    
    .bulk-actions .btn {
        width: 100%;
        margin-bottom: 0.5rem;
        padding: 0.75rem;
        font-size: 0.875rem;
    }
    
    /* Mobile Typography */
    h1 { font-size: 1.5rem; }
    h2 { font-size: 1.25rem; }
    h3 { font-size: 1.125rem; }
    h4 { font-size: 1rem; }
    
    .btn {
        padding: 0.625rem 1rem;
        font-size: 0.875rem;
        min-height: 44px; /* Touch target size */
    }
    
    /* Mobile Specific Utilities */
    .mobile-only {
        display: block;
    }
    
    .desktop-only {
        display: none;
    }
    
    .mobile-full-width {
        width: 100vw;
        margin-left: calc(-50vw + 50%);
    }
    
    .mobile-padding {
        padding-left: 0.75rem;
        padding-right: 0.75rem;
    }
    
    /* iOS Safari specific fixes */
    .ios-safari-fix {
        height: -webkit-fill-available;
    }
    
    /* Prevent horizontal scroll on small screens */
    body {
        overflow-x: hidden;
    }
}

/* Default - hide mobile-only elements */
@media (min-width: 576px) {
    .mobile-only {
        display: none;
    }
    
    .desktop-only {
        display: block;
    }
    
    .mobile-back-btn {
        display: none;
    }
}

/* Touch device optimizations */
@media (hover: none) and (pointer: coarse) {
    .btn {
        min-height: 44px;
        min-width: 44px;
    }
    
    .chat-item {
        min-height: 60px;
    }
    
    .message-actions {
        position: static;
        opacity: 1;
        margin-top: 0.5rem;
    }
    
    .chat-actions {
        opacity: 1;
    }
    
    /* Remove hover effects on touch devices */
    .hover-lift:hover,
    .hover-grow:hover,
    .hover-shrink:hover,
    .hover-rotate:hover {
        transform: none;
    }
}

/* High DPI displays */
@media (-webkit-min-device-pixel-ratio: 2), (min-resolution: 192dpi) {
    .avatar-img,
    .message-image {
        image-rendering: -webkit-optimize-contrast;
        image-rendering: crisp-edges;
    }
}

/* Landscape phone orientation */
@media (max-height: 500px) and (orientation: landscape) {
    .chat-sidebar {
        height: 150px;
    }
    
    .top-bar {
        padding: 0.5rem;
    }
    
    .message-input-container {
        padding: 0.5rem;
    }
    
    .modal-body {
        max-height: 60vh;
    }
}

/* Print styles */
@media print {
    .chat-sidebar,
    .message-input-container,
    .top-bar,
    .bulk-actions,
    .modal-overlay {
        display: none !important;
    }
    
    .main-content {
        flex-direction: column;
    }
    
    .chat-panel {
        width: 100%;
        border: none;
    }
    
    .message-bubble {
        max-width: 100%;
        break-inside: avoid;
        page-break-inside: avoid;
    }
    
    .message-content {
        border: 1px solid #000;
        box-shadow: none;
    }
}
"""
        }
    ]

    # Function to create files
    def create_files(files_list):
        print("\nCreating CSS files...")

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

    # Create all CSS files
    create_files(css_files)

    print("\n" + "="*70)
    print("CSS files created successfully!")
    print("="*70)

    print("\nCreated CSS Files:")
    print("✓ main.css - Global styles, variables, and base components")
    print("✓ chat.css - Chat interface, messages, and real-time features")
    print("✓ sidebar.css - Chat sidebar, user list, and navigation")
    print("✓ modal.css - Modal dialogs, popups, and overlays")
    print("✓ animations.css - Smooth transitions and visual effects")
    print("✓ responsive.css - Mobile-first responsive design")

    print("\nDesign Features:")
    print("• Modern, clean Reddit-inspired color scheme")
    print("• CSS custom properties (variables) for easy theming")
    print("• Smooth animations and hover effects")
    print("• Responsive design for all screen sizes")
    print("• Touch-friendly interface for mobile devices")
    print("• Accessibility considerations")
    print("• Print stylesheet support")

    print("\nChat-Specific Features:")
    print("• Message bubbles with different styles for own/other messages")
    print("• Typing indicators with animated dots")
    print("• Image message hide/show functionality")
    print("• File attachment styling")
    print("• System message differentiation")
    print("• Unread message indicators")
    print("• Pin/unpin visual feedback")
    print("• Bulk selection mode")

    print("\nResponsive Breakpoints:")
    print("• xs: 0-575px (phones)")
    print("• sm: 576-767px (large phones)")
    print("• md: 768-991px (tablets)")
    print("• lg: 992-1199px (desktops)")
    print("• xl: 1200px+ (large desktops)")

    print("\nAnimation Classes Available:")
    print("• .fade-in, .fade-out, .fade-in-up, .fade-in-down")
    print("• .scale-in, .scale-out, .bounce-in")
    print("• .slide-in-left, .slide-in-right, .slide-in-up")
    print("• .pulse, .shake, .rotate, .glow")
    print("• .hover-lift, .hover-grow, .hover-shrink")

    print("\nNext steps:")
    print("1. Link these CSS files in your HTML templates")
    print("2. Test the responsive design on different screen sizes")
    print("3. Customize the color scheme in main.css variables")
    print("4. Test animations and transitions")
    print("5. Verify accessibility and print styles")

if __name__ == "__main__":
    create_css_files()
