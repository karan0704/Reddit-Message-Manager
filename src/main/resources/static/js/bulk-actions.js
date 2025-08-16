// Bulk actions functionality
console.log('Bulk actions module loaded');

// Bulk actions state
let bulkMode = false;
let selectedItems = new Set();
let bulkActionType = null;

/**
 * Initialize bulk actions
 */
function initializeBulkActions() {
    setupBulkActionListeners();
    updateBulkActionButtons();
}

/**
 * Setup bulk action event listeners
 */
function setupBulkActionListeners() {
    // Bulk select toggle button
    const bulkSelectBtn = document.getElementById('bulkSelectBtn');
    if (bulkSelectBtn) {
        bulkSelectBtn.addEventListener('click', toggleBulkMode);
    }
    
    // Select all checkbox
    const selectAllCheckbox = document.getElementById('selectAllCheckbox');
    if (selectAllCheckbox) {
        selectAllCheckbox.addEventListener('change', handleSelectAll);
    }
    
    // Individual item checkboxes (delegated)
    document.addEventListener('change', function(e) {
        if (e.target.classList.contains('chat-select-checkbox') || 
            e.target.classList.contains('message-select-checkbox')) {
            handleItemSelection(e.target);
        }
    });
}

/**
 * Toggle bulk mode
 */
function toggleBulkMode() {
    bulkMode = !bulkMode;
    selectedItems.clear();
    
    const bulkSelectBtn = document.getElementById('bulkSelectBtn');
    const bulkActions = document.getElementById('bulkActions');
    const selectAllContainer = document.getElementById('selectAllContainer');
    
    // Update UI
    if (bulkSelectBtn) {
        bulkSelectBtn.classList.toggle('active', bulkMode);
        bulkSelectBtn.textContent = bulkMode ? 'Cancel' : 'Select';
    }
    
    if (bulkActions) {
        bulkActions.classList.toggle('hidden', !bulkMode);
    }
    
    if (selectAllContainer) {
        selectAllContainer.classList.toggle('hidden', !bulkMode);
    }
    
    // Show/hide checkboxes
    document.body.classList.toggle('bulk-mode', bulkMode);
    
    // Clear all selections when exiting bulk mode
    if (!bulkMode) {
        clearAllSelections();
    }
    
    updateBulkActionButtons();
}

/**
 * Handle select all checkbox
 */
function handleSelectAll(event) {
    const isChecked = event.target.checked;
    const checkboxes = document.querySelectorAll('.chat-select-checkbox, .message-select-checkbox');
    
    checkboxes.forEach(checkbox => {
        checkbox.checked = isChecked;
        handleItemSelection(checkbox);
    });
}

/**
 * Handle individual item selection
 */
function handleItemSelection(checkbox) {
    const itemId = getItemIdFromCheckbox(checkbox);
    const isSelected = checkbox.checked;
    
    if (isSelected) {
        selectedItems.add(itemId);
    } else {
        selectedItems.delete(itemId);
    }
    
    // Update item visual state
    const itemElement = checkbox.closest('.chat-item, .message-bubble');
    if (itemElement) {
        itemElement.classList.toggle('selected', isSelected);
    }
    
    updateBulkActionButtons();
    updateSelectAllCheckbox();
}

/**
 * Get item ID from checkbox
 */
function getItemIdFromCheckbox(checkbox) {
    const itemElement = checkbox.closest('.chat-item, .message-bubble');
    if (itemElement) {
        return itemElement.dataset.chatId || itemElement.dataset.messageId;
    }
    return checkbox.id;
}

/**
 * Update bulk action buttons state
 */
function updateBulkActionButtons() {
    const selectedCount = selectedItems.size;
    const bulkActionButtons = document.querySelectorAll('.bulk-action-btn');
    const selectedCountElement = document.getElementById('selectedCount');
    
    // Update selected count
    if (selectedCountElement) {
        selectedCountElement.textContent = selectedCount;
    }
    
    // Enable/disable bulk action buttons
    bulkActionButtons.forEach(btn => {
        const isCancel = btn.classList.contains('cancel-bulk-btn');
        btn.disabled = !isCancel && selectedCount === 0;
    });
    
    // Update bulk actions visibility
    const bulkActionsContainer = document.getElementById('bulkActions');
    if (bulkActionsContainer) {
        const hasSelection = selectedCount > 0;
        bulkActionsContainer.classList.toggle('has-selection', hasSelection);
    }
}

/**
 * Update select all checkbox state
 */
function updateSelectAllCheckbox() {
    const selectAllCheckbox = document.getElementById('selectAllCheckbox');
    if (!selectAllCheckbox) return;
    
    const allCheckboxes = document.querySelectorAll('.chat-select-checkbox:not(#selectAllCheckbox), .message-select-checkbox');
    const checkedCheckboxes = document.querySelectorAll('.chat-select-checkbox:checked, .message-select-checkbox:checked');
    
    if (allCheckboxes.length === 0) {
        selectAllCheckbox.indeterminate = false;
        selectAllCheckbox.checked = false;
    } else if (checkedCheckboxes.length === allCheckboxes.length) {
        selectAllCheckbox.indeterminate = false;
        selectAllCheckbox.checked = true;
    } else if (checkedCheckboxes.length > 0) {
        selectAllCheckbox.indeterminate = true;
        selectAllCheckbox.checked = false;
    } else {
        selectAllCheckbox.indeterminate = false;
        selectAllCheckbox.checked = false;
    }
}

/**
 * Clear all selections
 */
function clearAllSelections() {
    selectedItems.clear();
    
    // Uncheck all checkboxes
    document.querySelectorAll('.chat-select-checkbox, .message-select-checkbox').forEach(checkbox => {
        checkbox.checked = false;
    });
    
    // Remove selected class from items
    document.querySelectorAll('.chat-item.selected, .message-bubble.selected').forEach(item => {
        item.classList.remove('selected');
    });
    
    updateBulkActionButtons();
    updateSelectAllCheckbox();
}

/**
 * Get selected item IDs
 */
function getSelectedItemIds() {
    return Array.from(selectedItems);
}

/**
 * Perform bulk delete action
 */
async function performBulkDelete() {
    const selectedIds = getSelectedItemIds();
    
    if (selectedIds.length === 0) {
        showNotification('No items selected', 'warning');
        return;
    }
    
    const confirmMessage = `Delete ${selectedIds.length} item(s)? This action cannot be undone.`;
    if (!confirm(confirmMessage)) {
        return;
    }
    
    try {
        const response = await fetch(`${CONFIG.API_BASE_URL}/chat/bulk-action`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                actionType: 'DELETE_CHATS',
                chatIds: selectedIds.map(id => parseInt(id))
            })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            showNotification(`Deleted ${data.processedCount} item(s)`, 'success');
            
            // Remove deleted items from UI
            selectedIds.forEach(id => {
                const item = document.querySelector(`[data-chat-id="${id}"], [data-message-id="${id}"]`);
                if (item) {
                    item.remove();
                }
            });
            
            // Exit bulk mode
            toggleBulkMode();
            
            // Refresh data
            if (typeof loadUserChats === 'function') {
                loadUserChats();
            }
            
        } else {
            throw new Error(data.error || 'Failed to delete items');
        }
        
    } catch (error) {
        console.error('Error performing bulk delete:', error);
        showNotification('Failed to delete items', 'error');
    }
}

/**
 * Perform bulk pin action
 */
async function performBulkPin() {
    const selectedIds = getSelectedItemIds();
    
    if (selectedIds.length === 0) {
        showNotification('No chats selected', 'warning');
        return;
    }
    
    try {
        const response = await fetch(`${CONFIG.API_BASE_URL}/chat/bulk-action`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                actionType: 'PIN_CHATS',
                chatIds: selectedIds.map(id => parseInt(id))
            })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            showNotification(`Pinned ${data.processedCount} chat(s)`, 'success');
            
            // Update UI
            selectedIds.forEach(id => {
                const chatItem = document.querySelector(`[data-chat-id="${id}"]`);
                if (chatItem) {
                    const indicators = chatItem.querySelector('.chat-indicators');
                    if (indicators && !indicators.querySelector('.pinned-indicator')) {
                        indicators.insertAdjacentHTML('afterbegin', '<span class="pinned-indicator">📌</span>');
                    }
                }
            });
            
            // Exit bulk mode
            toggleBulkMode();
            
            // Refresh data
            if (typeof loadUserChats === 'function') {
                loadUserChats();
            }
            
        } else {
            throw new Error(data.error || 'Failed to pin chats');
        }
        
    } catch (error) {
        console.error('Error performing bulk pin:', error);
        showNotification('Failed to pin chats', 'error');
    }
}

/**
 * Perform bulk unpin action
 */
async function performBulkUnpin() {
    const selectedIds = getSelectedItemIds();
    
    if (selectedIds.length === 0) {
        showNotification('No chats selected', 'warning');
        return;
    }
    
    try {
        const response = await fetch(`${CONFIG.API_BASE_URL}/chat/bulk-action`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                actionType: 'UNPIN_CHATS',
                chatIds: selectedIds.map(id => parseInt(id))
            })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            showNotification(`Unpinned ${data.processedCount} chat(s)`, 'success');
            
            // Update UI
            selectedIds.forEach(id => {
                const chatItem = document.querySelector(`[data-chat-id="${id}"]`);
                if (chatItem) {
                    const pinnedIndicator = chatItem.querySelector('.pinned-indicator');
                    if (pinnedIndicator) {
                        pinnedIndicator.remove();
                    }
                }
            });
            
            // Exit bulk mode
            toggleBulkMode();
            
            // Refresh data
            if (typeof loadUserChats === 'function') {
                loadUserChats();
            }
            
        } else {
            throw new Error(data.error || 'Failed to unpin chats');
        }
        
    } catch (error) {
        console.error('Error performing bulk unpin:', error);
        showNotification('Failed to unpin chats', 'error');
    }
}

/**
 * Perform bulk archive action
 */
async function performBulkArchive() {
    const selectedIds = getSelectedItemIds();
    
    if (selectedIds.length === 0) {
        showNotification('No chats selected', 'warning');
        return;
    }
    
    try {
        const response = await fetch(`${CONFIG.API_BASE_URL}/chat/bulk-action`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                actionType: 'ARCHIVE_CHATS',
                chatIds: selectedIds.map(id => parseInt(id))
            })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            showNotification(`Archived ${data.processedCount} chat(s)`, 'success');
            
            // Remove archived chats from current view (if not showing archived)
            const showArchived = document.querySelector('[data-filter="archived"]')?.classList.contains('active');
            if (!showArchived) {
                selectedIds.forEach(id => {
                    const chatItem = document.querySelector(`[data-chat-id="${id}"]`);
                    if (chatItem) {
                        chatItem.remove();
                    }
                });
            }
            
            // Exit bulk mode
            toggleBulkMode();
            
            // Refresh data
            if (typeof loadUserChats === 'function') {
                loadUserChats();
            }
            
        } else {
            throw new Error(data.error || 'Failed to archive chats');
        }
        
    } catch (error) {
        console.error('Error performing bulk archive:', error);
        showNotification('Failed to archive chats', 'error');
    }
}

/**
 * Perform bulk block action
 */
async function performBulkBlock() {
    const selectedIds = getSelectedItemIds();
    
    if (selectedIds.length === 0) {
        showNotification('No chats selected', 'warning');
        return;
    }
    
    // Get usernames from selected chats
    const usernames = selectedIds.map(id => {
        const chatItem = document.querySelector(`[data-chat-id="${id}"]`);
        return chatItem?.querySelector('.chat-username')?.textContent;
    }).filter(Boolean);
    
    if (usernames.length === 0) {
        showNotification('No valid users to block', 'error');
        return;
    }
    
    const confirmMessage = `Block ${usernames.length} user(s)? You won't receive messages from them.`;
    if (!confirm(confirmMessage)) {
        return;
    }
    
    try {
        const response = await fetch(`${CONFIG.API_BASE_URL}/block/bulk-block`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                usernames: usernames,
                reason: 'Bulk block action'
            })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            showNotification(`Blocked ${data.blockedCount} user(s)`, 'success');
            
            // Remove blocked chats from UI
            selectedIds.forEach(id => {
                const chatItem = document.querySelector(`[data-chat-id="${id}"]`);
                if (chatItem) {
                    chatItem.remove();
                }
            });
            
            // Exit bulk mode
            toggleBulkMode();
            
            // Refresh data
            if (typeof loadUserChats === 'function') {
                loadUserChats();
            }
            
        } else {
            throw new Error(data.error || 'Failed to block users');
        }
        
    } catch (error) {
        console.error('Error performing bulk block:', error);
        showNotification('Failed to block users', 'error');
    }
}

/**
 * Show bulk action confirmation modal
 */
function showBulkActionConfirmation(actionType) {
    const selectedCount = selectedItems.size;
    if (selectedCount === 0) {
        showNotification('No items selected', 'warning');
        return;
    }
    
    let actionText = '';
    let warningText = '';
    
    switch (actionType) {
        case 'delete':
            actionText = 'Delete';
            warningText = 'This action cannot be undone.';
            break;
        case 'block':
            actionText = 'Block';
            warningText = 'You will no longer receive messages from these users.';
            break;
        case 'archive':
            actionText = 'Archive';
            warningText = 'These chats will be moved to archived.';
            break;
    }
    
    const modalHtml = `
        <div class="modal-overlay">
            <div class="modal modal-medium">
                <div class="modal-header">
                    <h3 class="modal-title">Confirm Bulk ${actionText}</h3>
                    <button class="modal-close" onclick="closeModal()">&times;</button>
                </div>
                <div class="modal-body">
                    <p>${actionText} ${selectedCount} selected item(s)?</p>
                    <p class="warning-text">${warningText}</p>
                </div>
                <div class="modal-footer">
                    <button onclick="closeModal()" class="btn btn-secondary">Cancel</button>
                    <button onclick="confirmBulkAction('${actionType}')" class="btn btn-danger">${actionText}</button>
                </div>
            </div>
        </div>
    `;
    
    document.body.insertAdjacentHTML('beforeend', modalHtml);
    setTimeout(() => document.querySelector('.modal-overlay').classList.add('show'), 10);
}

/**
 * Confirm bulk action
 */
function confirmBulkAction(actionType) {
    closeModal();
    
    switch (actionType) {
        case 'delete':
            performBulkDelete();
            break;
        case 'pin':
            performBulkPin();
            break;
        case 'unpin':
            performBulkUnpin();
            break;
        case 'archive':
            performBulkArchive();
            break;
        case 'block':
            performBulkBlock();
            break;
    }
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', initializeBulkActions);

// Export bulk actions functions
window.ChatApp = {
    ...window.ChatApp,
    toggleBulkMode,
    performBulkDelete,
    performBulkPin,
    performBulkUnpin,
    performBulkArchive,
    performBulkBlock,
    clearAllSelections,
    getSelectedItemIds
};

console.log('Bulk actions module loaded successfully');
