// Export functionality
console.log('Export module loaded');

// Export state
let currentExportId = null;
let exportStatusInterval = null;

/**
 * Show export modal
 */
function showExportModal() {
    const modalHtml = `
        <div class="modal-overlay">
            <div class="modal modal-large">
                <div class="modal-header">
                    <h3 class="modal-title">Export Chats</h3>
                    <button class="modal-close" onclick="closeModal()">&times;</button>
                </div>
                <div class="modal-body export-modal">
                    <div class="export-options">
                        <div class="export-option" data-format="TXT" onclick="selectExportFormat('TXT')">
                            <h5>📄 Text File</h5>
                            <p>Plain text format, easy to read</p>
                        </div>
                        <div class="export-option" data-format="JSON" onclick="selectExportFormat('JSON')">
                            <h5>📋 JSON File</h5>
                            <p>Structured data with metadata</p>
                        </div>
                        <div class="export-option" data-format="CSV" onclick="selectExportFormat('CSV')">
                            <h5>📊 CSV File</h5>
                            <p>Spreadsheet compatible format</p>
                        </div>
                    </div>
                    
                    <div class="export-settings">
                        <h4>Export Settings</h4>
                        
                        <div class="setting-group">
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
                            </div>
                        </div>
                        
                        <div class="setting-group">
                            <label>Date Range:</label>
                            <div class="date-range">
                                <input type="date" id="exportDateFrom" placeholder="From">
                                <input type="date" id="exportDateTo" placeholder="To">
                            </div>
                            <div class="quick-dates">
                                <button onclick="setExportDateRange('week')" class="btn btn-small">Last Week</button>
                                <button onclick="setExportDateRange('month')" class="btn btn-small">Last Month</button>
                                <button onclick="setExportDateRange('all')" class="btn btn-small">All Time</button>
                            </div>
                        </div>
                        
                        <div class="setting-group">
                            <label>Options:</label>
                            <div class="checkbox-group">
                                <label class="checkbox-label">
                                    <input type="checkbox" id="includeImages" checked>
                                    <span class="checkmark"></span>
                                    Include Images
                                </label>
                                <label class="checkbox-label">
                                    <input type="checkbox" id="includeMetadata" checked>
                                    <span class="checkmark"></span>
                                    Include Metadata
                                </label>
                                <label class="checkbox-label">
                                    <input type="checkbox" id="includeSystemMessages">
                                    <span class="checkmark"></span>
                                    Include System Messages
                                </label>
                            </div>
                        </div>
                        
                        <div class="setting-group">
                            <label for="maxMessages">Maximum Messages:</label>
                            <input type="number" id="maxMessages" value="1000" min="1" max="10000">
                            <small>Leave empty for no limit</small>
                        </div>
                    </div>
                </div>
                <div class="modal-footer">
                    <button onclick="closeModal()" class="btn btn-secondary">Cancel</button>
                    <button onclick="startExport()" class="btn btn-primary" id="startExportBtn" disabled>Start Export</button>
                </div>
            </div>
        </div>
    `;
    
    document.body.insertAdjacentHTML('beforeend', modalHtml);
    setTimeout(() => document.querySelector('.modal-overlay').classList.add('show'), 10);
}

/**
 * Select export format
 */
function selectExportFormat(format) {
    // Remove previous selection
    document.querySelectorAll('.export-option').forEach(option => {
        option.classList.remove('selected');
    });
    
    // Select new format
    const selectedOption = document.querySelector(`[data-format="${format}"]`);
    if (selectedOption) {
        selectedOption.classList.add('selected');
    }
    
    // Enable start button
    const startBtn = document.getElementById('startExportBtn');
    if (startBtn) {
        startBtn.disabled = false;
    }
}

/**
 * Set export date range
 */
function setExportDateRange(range) {
    const fromInput = document.getElementById('exportDateFrom');
    const toInput = document.getElementById('exportDateTo');
    
    if (!fromInput || !toInput) return;
    
    const now = new Date();
    const today = now.toISOString().split('T')[0];
    
    toInput.value = today;
    
    switch (range) {
        case 'week':
            const weekAgo = new Date(now.getTime() - 7 * 24 * 60 * 60 * 1000);
            fromInput.value = weekAgo.toISOString().split('T')[0];
            break;
        case 'month':
            const monthAgo = new Date(now.getFullYear(), now.getMonth() - 1, now.getDate());
            fromInput.value = monthAgo.toISOString().split('T')[0];
            break;
        case 'all':
            fromInput.value = '';
            toInput.value = '';
            break;
    }
}

/**
 * Start export process
 */
async function startExport() {
    const selectedFormat = document.querySelector('.export-option.selected');
    if (!selectedFormat) {
        showNotification('Please select an export format', 'warning');
        return;
    }
    
    const exportFormat = selectedFormat.dataset.format;
    const exportData = getExportData();
    
    try {
        const response = await fetch(`${CONFIG.API_BASE_URL}/export/chats`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                exportFormat: exportFormat,
                ...exportData
            })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            currentExportId = data.export.exportId;
            closeModal();
            showExportProgress(data.export);
            startExportStatusPolling();
        } else {
            throw new Error(data.error || 'Failed to start export');
        }
        
    } catch (error) {
        console.error('Error starting export:', error);
        showNotification('Failed to start export', 'error');
    }
}

/**
 * Get export data from form
 */
function getExportData() {
    const chatSelection = document.querySelector('input[name="chatSelection"]:checked')?.value || 'all';
    const dateFrom = document.getElementById('exportDateFrom')?.value;
    const dateTo = document.getElementById('exportDateTo')?.value;
    const includeImages = document.getElementById('includeImages')?.checked || false;
    const includeMetadata = document.getElementById('includeMetadata')?.checked || false;
    const includeSystemMessages = document.getElementById('includeSystemMessages')?.checked || false;
    const maxMessages = document.getElementById('maxMessages')?.value;
    
    const exportData = {
        chatSelection: chatSelection,
        includeImages: includeImages,
        includeMetadata: includeMetadata,
        includeSystemMessages: includeSystemMessages
    };
    
    if (dateFrom) exportData.dateFrom = new Date(dateFrom).toISOString();
    if (dateTo) exportData.dateTo = new Date(dateTo).toISOString();
    if (maxMessages) exportData.maxMessages = parseInt(maxMessages);
    
    // Get chat IDs based on selection
    if (chatSelection === 'selected') {
        exportData.chatIds = getSelectedItemIds();
    } else if (chatSelection === 'pinned') {
        const pinnedChats = document.querySelectorAll('.chat-item .pinned-indicator');
        exportData.chatIds = Array.from(pinnedChats).map(indicator => {
            const chatItem = indicator.closest('.chat-item');
            return parseInt(chatItem.dataset.chatId);
        });
    }
    
    return exportData;
}

/**
 * Show export progress modal
 */
function showExportProgress(exportInfo) {
    const modalHtml = `
        <div class="modal-overlay">
            <div class="modal modal-medium">
                <div class="modal-header">
                    <h3 class="modal-title">Exporting Chats</h3>
                </div>
                <div class="modal-body progress-modal">
                    <div class="export-info">
                        <p>Format: <strong>${exportInfo.exportFormat}</strong></p>
                        <p>Started: <strong>${formatDate(exportInfo.createdAt)}</strong></p>
                    </div>
                    
                    <div class="progress-container">
                        <div class="progress-bar">
                            <div class="progress-fill" id="exportProgressFill" style="width: 0%"></div>
                        </div>
                        <div class="progress-text" id="exportProgressText">Preparing export...</div>
                    </div>
                    
                    <div class="export-status" id="exportStatus">
                        <p>Status: <span id="exportStatusText">In Progress</span></p>
                        <p id="exportDetails"></p>
                    </div>
                </div>
                <div class="modal-footer">
                    <button onclick="cancelExport()" class="btn btn-secondary">Cancel</button>
                    <button onclick="closeModal()" class="btn btn-primary" id="closeProgressBtn" disabled>Close</button>
                </div>
            </div>
        </div>
    `;
    
    document.body.insertAdjacentHTML('beforeend', modalHtml);
    setTimeout(() => document.querySelector('.modal-overlay').classList.add('show'), 10);
}

/**
 * Start export status polling
 */
function startExportStatusPolling() {
    exportStatusInterval = setInterval(async () => {
        try {
            const response = await fetch(`${CONFIG.API_BASE_URL}/export/status/${currentExportId}`);
            const data = await response.json();
            
            if (response.ok) {
                updateExportProgress(data);
                
                if (data.exportStatus === 'COMPLETED') {
                    stopExportStatusPolling();
                    showExportComplete(data);
                } else if (data.exportStatus === 'FAILED') {
                    stopExportStatusPolling();
                    showExportError(data.errorMessage);
                }
            }
        } catch (error) {
            console.error('Error checking export status:', error);
        }
    }, 2000); // Poll every 2 seconds
}

/**
 * Stop export status polling
 */
function stopExportStatusPolling() {
    if (exportStatusInterval) {
        clearInterval(exportStatusInterval);
        exportStatusInterval = null;
    }
}

/**
 * Update export progress
 */
function updateExportProgress(exportData) {
    const progressFill = document.getElementById('exportProgressFill');
    const progressText = document.getElementById('exportProgressText');
    const statusText = document.getElementById('exportStatusText');
    const details = document.getElementById('exportDetails');
    
    if (progressFill && exportData.progress) {
        progressFill.style.width = exportData.progress + '%';
    }
    
    if (progressText) {
        progressText.textContent = exportData.statusMessage || 'Processing...';
    }
    
    if (statusText) {
        statusText.textContent = exportData.exportStatus || 'In Progress';
    }
    
    if (details && exportData.messageCount) {
        details.innerHTML = `Messages processed: <strong>${exportData.messageCount}</strong>`;
    }
}

/**
 * Show export complete
 */
function showExportComplete(exportData) {
    const progressText = document.getElementById('exportProgressText');
    const statusText = document.getElementById('exportStatusText');
    const closeBtn = document.getElementById('closeProgressBtn');
    const details = document.getElementById('exportDetails');
    
    if (progressText) {
        progressText.textContent = 'Export completed successfully!';
    }
    
    if (statusText) {
        statusText.textContent = 'Completed';
        statusText.style.color = 'var(--success-color)';
    }
    
    if (closeBtn) {
        closeBtn.disabled = false;
        closeBtn.textContent = 'Download';
        closeBtn.onclick = () => downloadExportFile(exportData.downloadUrl);
    }
    
    if (details) {
        details.innerHTML = `
            <p>Total messages: <strong>${exportData.messageCount}</strong></p>
            <p>File size: <strong>${formatFileSize(exportData.fileSize)}</strong></p>
            <p>Format: <strong>${exportData.exportFormat}</strong></p>
        `;
    }
    
    showNotification('Export completed successfully!', 'success');
}

/**
 * Show export error
 */
function showExportError(errorMessage) {
    const progressText = document.getElementById('exportProgressText');
    const statusText = document.getElementById('exportStatusText');
    const closeBtn = document.getElementById('closeProgressBtn');
    
    if (progressText) {
        progressText.textContent = 'Export failed';
    }
    
    if (statusText) {
        statusText.textContent = 'Failed';
        statusText.style.color = 'var(--danger-color)';
    }
    
    if (closeBtn) {
        closeBtn.disabled = false;
        closeBtn.textContent = 'Close';
    }
    
    showNotification(`Export failed: ${errorMessage}`, 'error');
}

/**
 * Cancel export
 */
async function cancelExport() {
    if (!currentExportId) return;
    
    try {
        const response = await fetch(`${CONFIG.API_BASE_URL}/export/cancel/${currentExportId}`, {
            method: 'POST'
        });
        
        if (response.ok) {
            stopExportStatusPolling();
            closeModal();
            showNotification('Export cancelled', 'info');
        }
    } catch (error) {
        console.error('Error cancelling export:', error);
    }
}

/**
 * Download export file
 */
function downloadExportFile(downloadUrl) {
    if (!downloadUrl) {
        showNotification('Download URL not available', 'error');
        return;
    }
    
    const link = document.createElement('a');
    link.href = downloadUrl;
    link.download = '';
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    
    closeModal();
    showNotification('Download started', 'success');
}

/**
 * Quick export current chat
 */
async function quickExportCurrentChat(format = 'TXT') {
    if (!activeChat) {
        showNotification('No active chat to export', 'warning');
        return;
    }
    
    try {
        const response = await fetch(`${CONFIG.API_BASE_URL}/export/chat/${activeChat.id}?format=${format}`);
        
        if (response.ok) {
            const blob = await response.blob();
            const url = URL.createObjectURL(blob);
            
            const link = document.createElement('a');
            link.href = url;
            link.download = `chat-${activeChat.otherUsername}-${new Date().toISOString().split('T')[0]}.${format.toLowerCase()}`;
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
            
            URL.revokeObjectURL(url);
            showNotification('Chat exported successfully', 'success');
        } else {
            throw new Error('Failed to export chat');
        }
    } catch (error) {
        console.error('Error exporting chat:', error);
        showNotification('Failed to export chat', 'error');
    }
}

// Export functions
window.ChatApp = {
    ...window.ChatApp,
    showExportModal,
    quickExportCurrentChat
};

console.log('Export module loaded successfully');
