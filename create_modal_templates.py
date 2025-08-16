import os

def create_modal_templates():
    # Base path from your previous conversation
    base_path = "D:\\Karan Ticket Project\\Reddit Message Manager"
    
    # Modal template files for the local chat application
    modal_templates = [
        {
            "path": "src\\main\\resources\\templates\\modals\\new-chat-modal.html",
            "content": """<!DOCTYPE html>
<html lang="en" xmlns:th="http://www.thymeleaf.org">
<head>
    <meta charset="UTF-8">
    <title>New Chat Modal</title>
</head>
<body>
    <!-- New Chat Modal Fragment -->
    <div th:fragment="new-chat-modal" class="modal-overlay" id="newChatModal" style="display: none;">
        <div class="modal modal-medium">
            <div class="modal-header">
                <h3 class="modal-title">Start New Chat</h3>
                <button class="modal-close" onclick="closeModal('newChatModal')">&times;</button>
            </div>
            
            <div class="modal-body">
                <div class="user-search-container">
                    <label for="newChatUserSearch">Search for users:</label>
                    <input type="text" 
                           id="newChatUserSearch" 
                           class="user-search-input" 
                           placeholder="Enter username or search..." 
                           autocomplete="off">
                    
                    <div id="newChatUserSuggestions" class="user-suggestions hidden">
                        <!-- Dynamic user suggestions will be populated here -->
                    </div>
                </div>
                
                <div id="newChatSelectedUser" class="selected-user hidden">
                    <div class="selected-user-info">
                        <img class="avatar-img" src="/images/default-avatar.png" alt="User Avatar">
                        <div class="user-details">
                            <h5 class="user-name">Selected User</h5>
                            <p class="user-username">@username</p>
                        </div>
                    </div>
                    <button onclick="clearSelectedUser()" class="btn btn-secondary">Change User</button>
                </div>
                
                <!-- Recent Users -->
                <div class="recent-users" th:if="${recentUsers}">
                    <h4>Recent Conversations</h4>
                    <div class="recent-users-list">
                        <div th:each="user : ${recentUsers}" 
                             class="recent-user-item" 
                             onclick="selectUserForChat(this)"
                             th:data-username="${user.username}"
                             th:data-display-name="${user.displayName}">
                            <img th:src="${user.avatarUrl ?: '/images/default-avatar.png'}" 
                                 th:alt="${user.username}" 
                                 class="avatar-img">
                            <div class="user-info">
                                <span class="user-name" th:text="${user.displayName ?: user.username}">Display Name</span>
                                <span class="user-status" th:text="${user.isOnline ? 'Online' : 'Offline'}" 
                                      th:class="${user.isOnline ? 'online' : 'offline'}">Status</span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            
            <div class="modal-footer">
                <button onclick="closeModal('newChatModal')" class="btn btn-secondary">Cancel</button>
                <button onclick="startNewChat()" class="btn btn-primary" id="startChatBtn" disabled>Start Chat</button>
            </div>
        </div>
    </div>
</body>
</html>
"""
        },
        
        {
            "path": "src\\main\\resources\\templates\\modals\\settings-modal.html",
            "content": """<!DOCTYPE html>
<html lang="en" xmlns:th="http://www.thymeleaf.org">
<head>
    <meta charset="UTF-8">
    <title>Settings Modal</title>
</head>
<body>
    <!-- Settings Modal Fragment -->
    <div th:fragment="settings-modal" class="modal-overlay" id="settingsModal" style="display: none;">
        <div class="modal modal-large">
            <div class="modal-header">
                <h3 class="modal-title">Settings</h3>
                <button class="modal-close" onclick="closeModal('settingsModal')">&times;</button>
            </div>
            
            <div class="modal-body settings-modal">
                <div class="settings-nav">
                    <div class="settings-nav-item active" onclick="showSettingsTab('general', this)">
                        <i class="icon-general">⚙️</i> General
                    </div>
                    <div class="settings-nav-item" onclick="showSettingsTab('notifications', this)">
                        <i class="icon-notifications">🔔</i> Notifications
                    </div>
                    <div class="settings-nav-item" onclick="showSettingsTab('privacy', this)">
                        <i class="icon-privacy">🔒</i> Privacy
                    </div>
                    <div class="settings-nav-item" onclick="showSettingsTab('appearance', this)">
                        <i class="icon-appearance">🎨</i> Appearance
                    </div>
                    <div class="settings-nav-item" onclick="showSettingsTab('advanced', this)">
                        <i class="icon-advanced">🔧</i> Advanced
                    </div>
                    <div class="settings-nav-item" onclick="showSettingsTab('about', this)">
                        <i class="icon-about">ℹ️</i> About
                    </div>
                </div>
                
                <div class="settings-content">
                    <!-- General Settings -->
                    <div id="generalSettings" class="settings-section">
                        <h4>General Settings</h4>
                        
                        <div class="setting-item">
                            <div class="setting-label">
                                <h5>Auto-scroll to new messages</h5>
                                <p>Automatically scroll to the bottom when new messages arrive</p>
                            </div>
                            <div class="setting-control">
                                <div class="toggle-switch active" onclick="toggleSetting(this, 'autoScroll')"></div>
                            </div>
                        </div>
                        
                        <div class="setting-item">
                            <div class="setting-label">
                                <h5>Send message with Enter</h5>
                                <p>Press Enter to send messages (Shift+Enter for new line)</p>
                            </div>
                            <div class="setting-control">
                                <div class="toggle-switch active" onclick="toggleSetting(this, 'enterToSend')"></div>
                            </div>
                        </div>
                        
                        <div class="setting-item">
                            <div class="setting-label">
                                <h5>Show typing indicators</h5>
                                <p>Show when others are typing</p>
                            </div>
                            <div class="setting-control">
                                <div class="toggle-switch active" onclick="toggleSetting(this, 'showTyping')"></div>
                            </div>
                        </div>
                        
                        <div class="setting-item">
                            <div class="setting-label">
                                <h5>Language</h5>
                                <p>Choose your preferred language</p>
                            </div>
                            <div class="setting-control">
                                <select class="setting-select" onchange="changeLanguage(this.value)">
                                    <option value="en">English</option>
                                    <option value="es">Español</option>
                                    <option value="fr">Français</option>
                                    <option value="de">Deutsch</option>
                                </select>
                            </div>
                        </div>
                    </div>
                    
                    <!-- Notifications Settings -->
                    <div id="notificationSettings" class="settings-section hidden">
                        <h4>Notification Settings</h4>
                        
                        <div class="setting-item">
                            <div class="setting-label">
                                <h5>Desktop notifications</h5>
                                <p>Show desktop notifications for new messages</p>
                            </div>
                            <div class="setting-control">
                                <div class="toggle-switch active" onclick="toggleSetting(this, 'desktopNotifications')"></div>
                            </div>
                        </div>
                        
                        <div class="setting-item">
                            <div class="setting-label">
                                <h5>Sound notifications</h5>
                                <p>Play sound when receiving new messages</p>
                            </div>
                            <div class="setting-control">
                                <div class="toggle-switch active" onclick="toggleSetting(this, 'soundNotifications')"></div>
                            </div>
                        </div>
                        
                        <div class="setting-item">
                            <div class="setting-label">
                                <h5>Notification sound</h5>
                                <p>Choose notification sound</p>
                            </div>
                            <div class="setting-control">
                                <select class="setting-select">
                                    <option value="default">Default</option>
                                    <option value="chime">Chime</option>
                                    <option value="bell">Bell</option>
                                    <option value="pop">Pop</option>
                                </select>
                            </div>
                        </div>
                        
                        <div class="setting-item">
                            <div class="setting-label">
                                <h5>Notification timeout</h5>
                                <p>How long notifications stay visible (seconds)</p>
                            </div>
                            <div class="setting-control">
                                <input type="range" min="3" max="10" value="5" class="setting-range">
                                <span class="range-value">5s</span>
                            </div>
                        </div>
                    </div>
                    
                    <!-- Privacy Settings -->
                    <div id="privacySettings" class="settings-section hidden">
                        <h4>Privacy Settings</h4>
                        
                        <div class="setting-item">
                            <div class="setting-label">
                                <h5>Hide images by default</h5>
                                <p>Hide image messages until clicked to view</p>
                            </div>
                            <div class="setting-control">
                                <div class="toggle-switch" onclick="toggleSetting(this, 'hideImages')"></div>
                            </div>
                        </div>
                        
                        <div class="setting-item">
                            <div class="setting-label">
                                <h5>Read receipts</h5>
                                <p>Send read receipts to other users</p>
                            </div>
                            <div class="setting-control">
                                <div class="toggle-switch active" onclick="toggleSetting(this, 'readReceipts')"></div>
                            </div>
                        </div>
                        
                        <div class="setting-item">
                            <div class="setting-label">
                                <h5>Online status</h5>
                                <p>Show your online status to others</p>
                            </div>
                            <div class="setting-control">
                                <div class="toggle-switch active" onclick="toggleSetting(this, 'showOnlineStatus')"></div>
                            </div>
                        </div>
                        
                        <div class="setting-item">
                            <div class="setting-label">
                                <h5>Block list</h5>
                                <p>Manage blocked users</p>
                            </div>
                            <div class="setting-control">
                                <button onclick="showBlockedUsersModal()" class="btn btn-secondary">Manage Blocked Users</button>
                            </div>
                        </div>
                    </div>
                    
                    <!-- Appearance Settings -->
                    <div id="appearanceSettings" class="settings-section hidden">
                        <h4>Appearance Settings</h4>
                        
                        <div class="setting-item">
                            <div class="setting-label">
                                <h5>Theme</h5>
                                <p>Choose your preferred theme</p>
                            </div>
                            <div class="setting-control">
                                <select class="setting-select" onchange="changeTheme(this.value)">
                                    <option value="light">Light</option>
                                    <option value="dark">Dark</option>
                                    <option value="auto">Auto (System)</option>
                                </select>
                            </div>
                        </div>
                        
                        <div class="setting-item">
                            <div class="setting-label">
                                <h5>Font size</h5>
                                <p>Adjust the size of text in messages</p>
                            </div>
                            <div class="setting-control">
                                <select class="setting-select" onchange="changeFontSize(this.value)">
                                    <option value="small">Small</option>
                                    <option value="medium" selected>Medium</option>
                                    <option value="large">Large</option>
                                </select>
                            </div>
                        </div>
                        
                        <div class="setting-item">
                            <div class="setting-label">
                                <h5>Chat density</h5>
                                <p>Adjust spacing between messages</p>
                            </div>
                            <div class="setting-control">
                                <select class="setting-select">
                                    <option value="compact">Compact</option>
                                    <option value="normal" selected>Normal</option>
                                    <option value="comfortable">Comfortable</option>
                                </select>
                            </div>
                        </div>
                    </div>
                    
                    <!-- Advanced Settings -->
                    <div id="advancedSettings" class="settings-section hidden">
                        <h4>Advanced Settings</h4>
                        
                        <div class="setting-item">
                            <div class="setting-label">
                                <h5>Developer mode</h5>
                                <p>Enable advanced debugging features</p>
                            </div>
                            <div class="setting-control">
                                <div class="toggle-switch" onclick="toggleSetting(this, 'developerMode')"></div>
                            </div>
                        </div>
                        
                        <div class="setting-item">
                            <div class="setting-label">
                                <h5>Export data</h5>
                                <p>Export your chat history and settings</p>
                            </div>
                            <div class="setting-control">
                                <button onclick="showExportModal()" class="btn btn-primary">Export Data</button>
                            </div>
                        </div>
                        
                        <div class="setting-item">
                            <div class="setting-label">
                                <h5>Clear cache</h5>
                                <p>Clear stored cache and temporary data</p>
                            </div>
                            <div class="setting-control">
                                <button onclick="clearCache()" class="btn btn-warning">Clear Cache</button>
                            </div>
                        </div>
                        
                        <div class="setting-item">
                            <div class="setting-label">
                                <h5>Reset settings</h5>
                                <p>Reset all settings to defaults</p>
                            </div>
                            <div class="setting-control">
                                <button onclick="resetSettings()" class="btn btn-danger">Reset All Settings</button>
                            </div>
                        </div>
                    </div>
                    
                    <!-- About Settings -->
                    <div id="aboutSettings" class="settings-section hidden">
                        <h4>About</h4>
                        
                        <div class="about-info">
                            <div class="app-logo">
                                <img src="/images/logo.png" alt="Reddit Chat Manager" class="logo-img">
                            </div>
                            
                            <h5>Reddit Chat Manager</h5>
                            <p class="version">Version 1.0.0</p>
                            <p class="description">A local chat application for managing Reddit-style conversations with modern features and real-time messaging.</p>
                            
                            <div class="about-links">
                                <button onclick="showKeyboardShortcuts()" class="btn btn-secondary">Keyboard Shortcuts</button>
                                <button onclick="showLicenseInfo()" class="btn btn-secondary">License</button>
                                <button onclick="checkForUpdates()" class="btn btn-secondary">Check for Updates</button>
                            </div>
                            
                            <div class="system-info">
                                <h6>System Information</h6>
                                <p>Browser: <span id="browserInfo">Chrome 91.0.4472.124</span></p>
                                <p>Platform: <span id="platformInfo">Windows 10</span></p>
                                <p>Connection: <span id="connectionStatus">Connected</span></p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            
            <div class="modal-footer">
                <button onclick="saveSettings()" class="btn btn-primary">Save Changes</button>
                <button onclick="closeModal('settingsModal')" class="btn btn-secondary">Close</button>
            </div>
        </div>
    </div>
</body>
</html>
"""
        },
        
        {
            "path": "src\\main\\resources\\templates\\modals\\export-modal.html",
            "content": """<!DOCTYPE html>
<html lang="en" xmlns:th="http://www.thymeleaf.org">
<head>
    <meta charset="UTF-8">
    <title>Export Modal</title>
</head>
<body>
    <!-- Export Modal Fragment -->
    <div th:fragment="export-modal" class="modal-overlay" id="exportModal" style="display: none;">
        <div class="modal modal-large">
            <div class="modal-header">
                <h3 class="modal-title">Export Chats</h3>
                <button class="modal-close" onclick="closeModal('exportModal')">&times;</button>
            </div>
            
            <div class="modal-body export-modal">
                <div class="export-options">
                    <div class="export-option" data-format="TXT" onclick="selectExportFormat('TXT', this)">
                        <div class="option-icon">📄</div>
                        <h5>Text File (.txt)</h5>
                        <p>Plain text format, easy to read and share</p>
                    </div>
                    
                    <div class="export-option" data-format="JSON" onclick="selectExportFormat('JSON', this)">
                        <div class="option-icon">📋</div>
                        <h5>JSON File (.json)</h5>
                        <p>Structured data with complete metadata</p>
                    </div>
                    
                    <div class="export-option" data-format="CSV" onclick="selectExportFormat('CSV', this)">
                        <div class="option-icon">📊</div>
                        <h5>CSV File (.csv)</h5>
                        <p>Spreadsheet compatible format</p>
                    </div>
                    
                    <div class="export-option" data-format="HTML" onclick="selectExportFormat('HTML', this)">
                        <div class="option-icon">🌐</div>
                        <h5>HTML File (.html)</h5>
                        <p>Web page format with styling</p>
                    </div>
                </div>
                
                <div class="export-settings">
                    <h4>Export Settings</h4>
                    
                    <div class="setting-row">
                        <label>Chat Selection:</label>
                        <div class="radio-group">
                            <label class="radio-label">
                                <input type="radio" name="chatSelection" value="all" checked>
                                <span class="radio-checkmark"></span>
                                All Chats
                            </label>
                            <label class="radio-label">
                                <input type="radio" name="chatSelection" value="selected">
                                <span class="radio-checkmark"></span>
                                Selected Chats Only
                            </label>
                            <label class="radio-label">
                                <input type="radio" name="chatSelection" value="pinned">
                                <span class="radio-checkmark"></span>
                                Pinned Chats Only
                            </label>
                            <label class="radio-label">
                                <input type="radio" name="chatSelection" value="current">
                                <span class="radio-checkmark"></span>
                                Current Chat Only
                            </label>
                        </div>
                    </div>
                    
                    <div class="setting-row">
                        <label>Date Range:</label>
                        <div class="date-range">
                            <div class="date-input-group">
                                <label for="exportDateFrom">From:</label>
                                <input type="date" id="exportDateFrom" class="date-input">
                            </div>
                            <div class="date-input-group">
                                <label for="exportDateTo">To:</label>
                                <input type="date" id="exportDateTo" class="date-input">
                            </div>
                        </div>
                        <div class="quick-dates">
                            <button onclick="setExportDateRange('week')" class="btn btn-small">Last Week</button>
                            <button onclick="setExportDateRange('month')" class="btn btn-small">Last Month</button>
                            <button onclick="setExportDateRange('year')" class="btn btn-small">Last Year</button>
                            <button onclick="setExportDateRange('all')" class="btn btn-small">All Time</button>
                        </div>
                    </div>
                    
                    <div class="setting-row">
                        <label>Include:</label>
                        <div class="checkbox-group">
                            <label class="checkbox-label">
                                <input type="checkbox" id="includeImages" checked>
                                <span class="checkmark"></span>
                                Images and Media
                            </label>
                            <label class="checkbox-label">
                                <input type="checkbox" id="includeMetadata" checked>
                                <span class="checkmark"></span>
                                Timestamps and Metadata
                            </label>
                            <label class="checkbox-label">
                                <input type="checkbox" id="includeSystemMessages">
                                <span class="checkmark"></span>
                                System Messages
                            </label>
                            <label class="checkbox-label">
                                <input type="checkbox" id="includeUserInfo" checked>
                                <span class="checkmark"></span>
                                User Information
                            </label>
                        </div>
                    </div>
                    
                    <div class="setting-row">
                        <label for="maxMessages">Message Limit:</label>
                        <div class="limit-input-group">
                            <input type="number" id="maxMessages" value="1000" min="1" max="50000" class="limit-input">
                            <select class="limit-select">
                                <option value="1000">1,000 messages</option>
                                <option value="5000">5,000 messages</option>
                                <option value="10000">10,000 messages</option>
                                <option value="0">No limit</option>
                            </select>
                        </div>
                        <small>Large exports may take longer to process</small>
                    </div>
                    
                    <div class="setting-row">
                        <label>File Options:</label>
                        <div class="checkbox-group">
                            <label class="checkbox-label">
                                <input type="checkbox" id="compressExport">
                                <span class="checkmark"></span>
                                Compress as ZIP file
                            </label>
                            <label class="checkbox-label">
                                <input type="checkbox" id="splitLargeFiles">
                                <span class="checkmark"></span>
                                Split large files
                            </label>
                        </div>
                    </div>
                </div>
                
                <div class="export-preview">
                    <h4>Export Preview</h4>
                    <div class="preview-info">
                        <p><strong>Format:</strong> <span id="previewFormat">Not selected</span></p>
                        <p><strong>Estimated size:</strong> <span id="previewSize">Calculating...</span></p>
                        <p><strong>Number of chats:</strong> <span id="previewChats">0</span></p>
                        <p><strong>Number of messages:</strong> <span id="previewMessages">0</span></p>
                    </div>
                </div>
            </div>
            
            <div class="modal-footer">
                <button onclick="closeModal('exportModal')" class="btn btn-secondary">Cancel</button>
                <button onclick="startExport()" class="btn btn-primary" id="startExportBtn" disabled>Start Export</button>
            </div>
        </div>
    </div>
    
    <!-- Export Progress Modal Fragment -->
    <div th:fragment="export-progress-modal" class="modal-overlay" id="exportProgressModal" style="display: none;">
        <div class="modal modal-medium">
            <div class="modal-header">
                <h3 class="modal-title">Exporting Chats</h3>
            </div>
            
            <div class="modal-body progress-modal">
                <div class="export-info">
                    <p>Format: <strong id="exportFormatInfo">JSON</strong></p>
                    <p>Started: <strong id="exportStartTime">Now</strong></p>
                </div>
                
                <div class="progress-container">
                    <div class="progress-bar">
                        <div class="progress-fill" id="exportProgressFill" style="width: 0%"></div>
                    </div>
                    <div class="progress-text" id="exportProgressText">Preparing export...</div>
                    <div class="progress-percentage" id="exportProgressPercentage">0%</div>
                </div>
                
                <div class="export-status" id="exportStatus">
                    <p>Status: <span id="exportStatusText">In Progress</span></p>
                    <p id="exportDetails">Processing messages...</p>
                    <p id="exportETA">Estimated time remaining: Calculating...</p>
                </div>
                
                <div class="export-log" id="exportLog">
                    <h5>Export Log:</h5>
                    <div class="log-content" id="exportLogContent">
                        <p>Export started...</p>
                    </div>
                </div>
            </div>
            
            <div class="modal-footer">
                <button onclick="cancelExport()" class="btn btn-danger" id="cancelExportBtn">Cancel Export</button>
                <button onclick="closeModal('exportProgressModal')" class="btn btn-primary" id="closeProgressBtn" disabled>Close</button>
            </div>
        </div>
    </div>
</body>
</html>
"""
        },
        
        {
            "path": "src\\main\\resources\\templates\\modals\\image-viewer-modal.html",
            "content": """<!DOCTYPE html>
<html lang="en" xmlns:th="http://www.thymeleaf.org">
<head>
    <meta charset="UTF-8">
    <title>Image Viewer Modal</title>
</head>
<body>
    <!-- Image Viewer Modal Fragment -->
    <div th:fragment="image-viewer-modal" class="modal-overlay image-viewer" id="imageViewerModal" style="display: none;">
        <div class="image-viewer-modal">
            <div class="image-viewer-content">
                <img id="viewerImage" src="" alt="Image" class="viewer-image">
                
                <div class="image-viewer-controls">
                    <button id="prevImageBtn" onclick="previousImage()" class="viewer-btn" title="Previous Image" style="display: none;">
                        <i class="icon-prev">⬅️</i>
                    </button>
                    
                    <button id="nextImageBtn" onclick="nextImage()" class="viewer-btn" title="Next Image" style="display: none;">
                        <i class="icon-next">➡️</i>
                    </button>
                    
                    <button onclick="zoomIn()" class="viewer-btn" title="Zoom In">
                        <i class="icon-zoom-in">🔍+</i>
                    </button>
                    
                    <button onclick="zoomOut()" class="viewer-btn" title="Zoom Out">
                        <i class="icon-zoom-out">🔍-</i>
                    </button>
                    
                    <button onclick="resetZoom()" class="viewer-btn" title="Reset Zoom">
                        <i class="icon-reset">🔄</i>
                    </button>
                    
                    <button onclick="rotateImage(90)" class="viewer-btn" title="Rotate Right">
                        <i class="icon-rotate">↻</i>
                    </button>
                    
                    <button onclick="downloadCurrentImage()" class="viewer-btn" title="Download">
                        <i class="icon-download">⬇️</i>
                    </button>
                    
                    <button onclick="shareImage()" class="viewer-btn" title="Share">
                        <i class="icon-share">📤</i>
                    </button>
                    
                    <button onclick="closeImageViewer()" class="viewer-btn close-btn" title="Close">
                        <i class="icon-close">✖️</i>
                    </button>
                </div>
                
                <div id="imageCounter" class="image-counter" style="display: none;">
                    <span id="currentImageIndex">1</span> of <span id="totalImages">1</span>
                </div>
                
                <div class="image-info" id="imageInfo">
                    <div class="info-item">
                        <span class="info-label">From:</span>
                        <span class="info-value" id="imageSender">Unknown</span>
                    </div>
                    <div class="info-item">
                        <span class="info-label">Date:</span>
                        <span class="info-value" id="imageDate">Unknown</span>
                    </div>
                    <div class="info-item">
                        <span class="info-label">Size:</span>
                        <span class="info-value" id="imageSize">Unknown</span>
                    </div>
                </div>
            </div>
            
            <!-- Image Thumbnails (for multiple images) -->
            <div id="imageThumbnails" class="image-thumbnails" style="display: none;">
                <div class="thumbnails-container" id="thumbnailsContainer">
                    <!-- Thumbnails will be populated dynamically -->
                </div>
            </div>
        </div>
    </div>
    
    <!-- Image Upload Modal Fragment -->
    <div th:fragment="image-upload-modal" class="modal-overlay" id="imageUploadModal" style="display: none;">
        <div class="modal modal-medium">
            <div class="modal-header">
                <h3 class="modal-title">Upload Image</h3>
                <button class="modal-close" onclick="closeModal('imageUploadModal')">&times;</button>
            </div>
            
            <div class="modal-body">
                <div class="upload-area" id="imageUploadArea">
                    <div class="upload-placeholder">
                        <i class="upload-icon">📷</i>
                        <h4>Choose Image or Drag & Drop</h4>
                        <p>Supports: JPEG, PNG, GIF, WebP (Max 10MB)</p>
                        <button onclick="document.getElementById('imageFileInput').click()" class="btn btn-primary">
                            Choose File
                        </button>
                        <input type="file" id="imageFileInput" accept="image/*" style="display: none;" onchange="handleImageFileSelect(this.files)">
                    </div>
                </div>
                
                <div class="image-preview" id="imagePreview" style="display: none;">
                    <img id="previewImage" src="" alt="Preview" class="preview-img">
                    <div class="preview-info">
                        <p><strong>File:</strong> <span id="previewFileName">image.jpg</span></p>
                        <p><strong>Size:</strong> <span id="previewFileSize">1.2 MB</span></p>
                        <p><strong>Dimensions:</strong> <span id="previewDimensions">1920x1080</span></p>
                    </div>
                    <div class="preview-actions">
                        <button onclick="clearImagePreview()" class="btn btn-secondary">Change Image</button>
                        <button onclick="compressImage()" class="btn btn-outline">Compress</button>
                    </div>
                </div>
                
                <div class="upload-options">
                    <div class="option-group">
                        <label class="checkbox-label">
                            <input type="checkbox" id="compressUpload" checked>
                            <span class="checkmark"></span>
                            Compress image for faster upload
                        </label>
                    </div>
                    <div class="option-group">
                        <label for="imageCaption">Caption (optional):</label>
                        <textarea id="imageCaption" placeholder="Add a caption for this image..." rows="2"></textarea>
                    </div>
                </div>
            </div>
            
            <div class="modal-footer">
                <button onclick="closeModal('imageUploadModal')" class="btn btn-secondary">Cancel</button>
                <button onclick="uploadSelectedImage()" class="btn btn-primary" id="uploadImageBtn" disabled>Upload Image</button>
            </div>
        </div>
    </div>
</body>
</html>
"""
        },
        
        {
            "path": "src\\main\\resources\\templates\\modals\\confirmation-modal.html",
            "content": """<!DOCTYPE html>
<html lang="en" xmlns:th="http://www.thymeleaf.org">
<head>
    <meta charset="UTF-8">
    <title>Confirmation Modal</title>
</head>
<body>
    <!-- Generic Confirmation Modal Fragment -->
    <div th:fragment="confirmation-modal" class="modal-overlay" id="confirmationModal" style="display: none;">
        <div class="modal modal-small">
            <div class="modal-header">
                <h3 class="modal-title" id="confirmationTitle">Confirm Action</h3>
                <button class="modal-close" onclick="closeModal('confirmationModal')">&times;</button>
            </div>
            
            <div class="modal-body">
                <div class="confirmation-icon" id="confirmationIcon">
                    <i class="icon-warning">⚠️</i>
                </div>
                <div class="confirmation-message" id="confirmationMessage">
                    <p>Are you sure you want to perform this action?</p>
                </div>
                <div class="confirmation-details" id="confirmationDetails" style="display: none;">
                    <p class="details-text">This action cannot be undone.</p>
                </div>
            </div>
            
            <div class="modal-footer">
                <button onclick="closeModal('confirmationModal')" class="btn btn-secondary" id="confirmationCancelBtn">Cancel</button>
                <button onclick="confirmAction()" class="btn btn-danger" id="confirmationConfirmBtn">Confirm</button>
            </div>
        </div>
    </div>
    
    <!-- Delete Chat Confirmation Modal Fragment -->
    <div th:fragment="delete-chat-modal" class="modal-overlay" id="deleteChatModal" style="display: none;">
        <div class="modal modal-small">
            <div class="modal-header">
                <h3 class="modal-title">Delete Chat</h3>
                <button class="modal-close" onclick="closeModal('deleteChatModal')">&times;</button>
            </div>
            
            <div class="modal-body">
                <div class="warning-icon">
                    <i class="icon-delete">🗑️</i>
                </div>
                <div class="warning-message">
                    <h4>Delete chat with <span id="deleteChatUsername">user</span>?</h4>
                    <p>This will permanently delete all messages in this conversation.</p>
                    <p class="warning-text"><strong>This action cannot be undone.</strong></p>
                </div>
                
                <div class="delete-options">
                    <label class="checkbox-label">
                        <input type="checkbox" id="deleteForBoth">
                        <span class="checkmark"></span>
                        Also delete for the other person (if possible)
                    </label>
                </div>
            </div>
            
            <div class="modal-footer">
                <button onclick="closeModal('deleteChatModal')" class="btn btn-secondary">Cancel</button>
                <button onclick="confirmDeleteChat()" class="btn btn-danger">Delete Chat</button>
            </div>
        </div>
    </div>
    
    <!-- Block User Confirmation Modal Fragment -->
    <div th:fragment="block-user-modal" class="modal-overlay" id="blockUserModal" style="display: none;">
        <div class="modal modal-medium">
            <div class="modal-header">
                <h3 class="modal-title">Block User</h3>
                <button class="modal-close" onclick="closeModal('blockUserModal')">&times;</button>
            </div>
            
            <div class="modal-body">
                <div class="block-icon">
                    <i class="icon-block">🚫</i>
                </div>
                <div class="block-message">
                    <h4>Block <span id="blockUsername">user</span>?</h4>
                    <p>Blocked users cannot send you messages or see when you're online.</p>
                </div>
                
                <div class="block-options">
                    <h5>Block Options:</h5>
                    <label class="checkbox-label">
                        <input type="checkbox" id="blockMessages" checked>
                        <span class="checkmark"></span>
                        Block messages from this user
                    </label>
                    <label class="checkbox-label">
                        <input type="checkbox" id="hideOnlineStatus" checked>
                        <span class="checkmark"></span>
                        Hide your online status from this user
                    </label>
                    <label class="checkbox-label">
                        <input type="checkbox" id="deleteExistingChat">
                        <span class="checkmark"></span>
                        Delete existing conversation
                    </label>
                </div>
                
                <div class="block-reason">
                    <label for="blockReason">Reason (optional):</label>
                    <select id="blockReason" class="block-reason-select">
                        <option value="">Select a reason...</option>
                        <option value="spam">Spam</option>
                        <option value="harassment">Harassment</option>
                        <option value="inappropriate">Inappropriate content</option>
                        <option value="unwanted">Unwanted contact</option>
                        <option value="other">Other</option>
                    </select>
                </div>
            </div>
            
            <div class="modal-footer">
                <button onclick="closeModal('blockUserModal')" class="btn btn-secondary">Cancel</button>
                <button onclick="confirmBlockUser()" class="btn btn-danger">Block User</button>
            </div>
        </div>
    </div>
    
    <!-- Logout Confirmation Modal Fragment -->
    <div th:fragment="logout-modal" class="modal-overlay" id="logoutModal" style="display: none;">
        <div class="modal modal-small">
            <div class="modal-header">
                <h3 class="modal-title">Logout</h3>
                <button class="modal-close" onclick="closeModal('logoutModal')">&times;</button>
            </div>
            
            <div class="modal-body">
                <div class="logout-icon">
                    <i class="icon-logout">🚪</i>
                </div>
                <div class="logout-message">
                    <h4>Are you sure you want to logout?</h4>
                    <p>You will need to login again to access your chats.</p>
                </div>
                
                <div class="logout-options">
                    <label class="checkbox-label">
                        <input type="checkbox" id="rememberLogin">
                        <span class="checkmark"></span>
                        Remember me for quick login next time
                    </label>
                </div>
            </div>
            
            <div class="modal-footer">
                <button onclick="closeModal('logoutModal')" class="btn btn-secondary">Cancel</button>
                <button onclick="confirmLogout()" class="btn btn-primary">Logout</button>
            </div>
        </div>
    </div>
</body>
</html>
"""
        },
        
        {
            "path": "src\\main\\resources\\templates\\modals\\user-profile-modal.html",
            "content": """<!DOCTYPE html>
<html lang="en" xmlns:th="http://www.thymeleaf.org">
<head>
    <meta charset="UTF-8">
    <title>User Profile Modal</title>
</head>
<body>
    <!-- User Profile Modal Fragment -->
    <div th:fragment="user-profile-modal" class="modal-overlay" id="userProfileModal" style="display: none;">
        <div class="modal modal-medium">
            <div class="modal-header">
                <h3 class="modal-title">User Profile</h3>
                <button class="modal-close" onclick="closeModal('userProfileModal')">&times;</button>
            </div>
            
            <div class="modal-body">
                <div class="profile-header">
                    <div class="profile-avatar">
                        <img id="profileAvatar" src="/images/default-avatar.png" alt="User Avatar" class="avatar-large">
                        <div class="status-indicator" id="profileStatus">
                            <span class="status-dot online"></span>
                            <span class="status-text">Online</span>
                        </div>
                    </div>
                    
                    <div class="profile-info">
                        <h4 id="profileDisplayName">Display Name</h4>
                        <p id="profileUsername">@username</p>
                        <p id="profileJoinDate">Member since: January 2024</p>
                    </div>
                </div>
                
                <div class="profile-stats">
                    <div class="stat-item">
                        <span class="stat-value" id="profileMessageCount">0</span>
                        <span class="stat-label">Messages</span>
                    </div>
                    <div class="stat-item">
                        <span class="stat-value" id="profileChatCount">0</span>
                        <span class="stat-label">Chats</span>
                    </div>
                    <div class="stat-item">
                        <span class="stat-value" id="profileLastSeen">Unknown</span>
                        <span class="stat-label">Last Seen</span>
                    </div>
                </div>
                
                <div class="profile-actions">
                    <button onclick="startChatWithUser()" class="btn btn-primary">
                        <i class="icon-chat">💬</i> Send Message
                    </button>
                    <button onclick="showBlockUserModal()" class="btn btn-danger">
                        <i class="icon-block">🚫</i> Block User
                    </button>
                    <button onclick="reportUser()" class="btn btn-warning">
                        <i class="icon-report">⚠️</i> Report
                    </button>
                </div>
                
                <div class="profile-details">
                    <div class="detail-section">
                        <h5>About</h5>
                        <p id="profileBio">No bio available.</p>
                    </div>
                    
                    <div class="detail-section" id="mutualChatsSection" style="display: none;">
                        <h5>Mutual Conversations</h5>
                        <div id="mutualChatsList">
                            <!-- Populated dynamically -->
                        </div>
                    </div>
                </div>
            </div>
            
            <div class="modal-footer">
                <button onclick="closeModal('userProfileModal')" class="btn btn-secondary">Close</button>
            </div>
        </div>
    </div>
    
    <!-- Edit Profile Modal Fragment -->
    <div th:fragment="edit-profile-modal" class="modal-overlay" id="editProfileModal" style="display: none;">
        <div class="modal modal-medium">
            <div class="modal-header">
                <h3 class="modal-title">Edit Profile</h3>
                <button class="modal-close" onclick="closeModal('editProfileModal')">&times;</button>
            </div>
            
            <div class="modal-body">
                <form id="editProfileForm">
                    <div class="avatar-edit">
                        <div class="current-avatar">
                            <img id="editProfileAvatar" src="/images/default-avatar.png" alt="Current Avatar" class="avatar-large">
                            <button type="button" onclick="changeAvatar()" class="change-avatar-btn">
                                <i class="icon-camera">📷</i>
                            </button>
                        </div>
                        <input type="file" id="avatarInput" accept="image/*" style="display: none;" onchange="handleAvatarChange(this.files)">
                    </div>
                    
                    <div class="form-group">
                        <label for="editDisplayName">Display Name:</label>
                        <input type="text" id="editDisplayName" name="displayName" maxlength="50" placeholder="Your display name">
                        <small>This is how others will see your name in chats</small>
                    </div>
                    
                    <div class="form-group">
                        <label for="editUsername">Username:</label>
                        <input type="text" id="editUsername" name="username" maxlength="30" placeholder="@username" readonly>
                        <small>Username cannot be changed</small>
                    </div>
                    
                    <div class="form-group">
                        <label for="editEmail">Email:</label>
                        <input type="email" id="editEmail" name="email" placeholder="your.email@example.com">
                        <small>Used for account recovery and notifications</small>
                    </div>
                    
                    <div class="form-group">
                        <label for="editBio">Bio:</label>
                        <textarea id="editBio" name="bio" rows="3" maxlength="200" placeholder="Tell others about yourself..."></textarea>
                        <small><span id="bioCharCount">0</span>/200 characters</small>
                    </div>
                    
                    <div class="form-group">
                        <label>Privacy Settings:</label>
                        <div class="privacy-options">
                            <label class="checkbox-label">
                                <input type="checkbox" id="showOnlineStatus" name="showOnlineStatus" checked>
                                <span class="checkmark"></span>
                                Show online status to others
                            </label>
                            <label class="checkbox-label">
                                <input type="checkbox" id="allowDirectMessages" name="allowDirectMessages" checked>
                                <span class="checkmark"></span>
                                Allow messages from anyone
                            </label>
                            <label class="checkbox-label">
                                <input type="checkbox" id="showReadReceipts" name="showReadReceipts" checked>
                                <span class="checkmark"></span>
                                Send read receipts
                            </label>
                        </div>
                    </div>
                </form>
            </div>
            
            <div class="modal-footer">
                <button onclick="closeModal('editProfileModal')" class="btn btn-secondary">Cancel</button>
                <button onclick="saveProfileChanges()" class="btn btn-primary">Save Changes</button>
            </div>
        </div>
    </div>
</body>
</html>
"""
        }
    ]
    
    # Function to create files
    def create_files(files_list):
        print("\nCreating modal template files...")
        
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
    
    # Create all modal template files
    create_files(modal_templates)
    
    print("\n" + "="*70)
    print("Modal templates created successfully!")
    print("="*70)
    
    print("\nCreated Modal Templates:")
    print("✓ new-chat-modal.html - Start new conversations with user search")
    print("✓ settings-modal.html - Comprehensive settings with tabbed interface")
    print("✓ export-modal.html - Export chats with format options and progress")
    print("✓ image-viewer-modal.html - Full-featured image viewer with controls")
    print("✓ confirmation-modal.html - Various confirmation dialogs")
    print("✓ user-profile-modal.html - User profiles and profile editing")
    
    print("\nModal Features:")
    print("• 🔍 New Chat - User search with autocomplete and recent contacts")
    print("• ⚙️ Settings - Tabbed interface with general, notifications, privacy, appearance")
    print("• 📤 Export - Multiple formats (TXT, JSON, CSV, HTML) with progress tracking")
    print("• 🖼️ Image Viewer - Zoom, rotate, navigate multiple images, download")
    print("• ⚠️ Confirmations - Delete chat, block user, logout with options")
    print("• 👤 User Profile - View profiles, edit own profile, privacy settings")
    
    print("\nThymeleaf Integration:")
    print("• Fragment-based templates for easy inclusion")
    print("• Server-side data binding with th: attributes")
    print("• Conditional rendering based on user permissions")
    print("• Form handling with validation")
    print("• Dynamic content population")
    
    print("\nAccessibility Features:")
    print("• Proper ARIA labels and roles")
    print("• Keyboard navigation support")
    print("• Screen reader friendly")
    print("• Focus management")
    print("• High contrast support")
    
    print("\nNext steps:")
    print("1. Include modal fragments in your main dashboard template")
    print("2. Add modal trigger buttons and JavaScript functions")
    print("3. Implement server-side endpoints for modal data")
    print("4. Test modal functionality and responsiveness")
    print("5. Add CSS styling to match your application theme")

if __name__ == "__main__":
    create_modal_templates()