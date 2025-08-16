// Image handling functionality
console.log('Image handler module loaded');

// Image handler state
let imageViewerOpen = false;
let currentImageIndex = 0;
let currentImageList = [];

/**
 * Initialize image handling
 */
function initializeImageHandler() {
    setupImageUploadHandler();
    setupImageViewerKeyboardEvents();
    setupImageLazyLoading();
}

/**
 * Setup image upload handler
 */
function setupImageUploadHandler() {
    // File input for image upload
    const imageInput = document.getElementById('imageInput');
    if (imageInput) {
        imageInput.addEventListener('change', handleImageUpload);
    }
    
    // Drag and drop for image upload
    const messageInput = document.getElementById('messageInput');
    if (messageInput) {
        messageInput.addEventListener('dragover', handleDragOver);
        messageInput.addEventListener('drop', handleImageDrop);
    }
    
    // Paste event for images
    document.addEventListener('paste', handleImagePaste);
}

/**
 * Handle image upload
 */
async function handleImageUpload(event) {
    const files = event.target.files;
    if (!files || files.length === 0) return;
    
    for (const file of files) {
        if (file.type.startsWith('image/')) {
            await uploadAndSendImage(file);
        } else {
            showNotification('Please select image files only', 'warning');
        }
    }
    
    // Clear input
    event.target.value = '';
}

/**
 * Handle drag over
 */
function handleDragOver(event) {
    event.preventDefault();
    event.currentTarget.classList.add('drag-over');
}

/**
 * Handle image drop
 */
function handleImageDrop(event) {
    event.preventDefault();
    event.currentTarget.classList.remove('drag-over');
    
    const files = event.dataTransfer.files;
    if (!files || files.length === 0) return;
    
    for (const file of files) {
        if (file.type.startsWith('image/')) {
            uploadAndSendImage(file);
        } else {
            showNotification('Please drop image files only', 'warning');
        }
    }
}

/**
 * Handle image paste
 */
function handleImagePaste(event) {
    const items = event.clipboardData?.items;
    if (!items) return;
    
    for (const item of items) {
        if (item.type.startsWith('image/')) {
            const file = item.getAsFile();
            if (file) {
                uploadAndSendImage(file);
            }
        }
    }
}

/**
 * Upload and send image
 */
async function uploadAndSendImage(file) {
    if (!activeChat) {
        showNotification('Please select a chat first', 'warning');
        return;
    }
    
    // Validate file size (max 10MB)
    const maxSize = 10 * 1024 * 1024;
    if (file.size > maxSize) {
        showNotification('Image is too large. Maximum size is 10MB', 'error');
        return;
    }
    
    try {
        // Show upload progress
        const messageId = 'temp_' + Date.now();
        showImageUploadProgress(messageId, file);
        
        // Create form data
        const formData = new FormData();
        formData.append('image', file);
        formData.append('chatId', activeChat.id);
        
        // Upload image
        const response = await fetch(`${CONFIG.API_BASE_URL}/upload/image`, {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        
        if (response.ok) {
            // Remove progress indicator
            removeImageUploadProgress(messageId);
            
            // Send image message
            const messageData = {
                messageContent: '',
                messageType: 'IMAGE',
                imageUrl: data.imageUrl
            };
            
            const messageResponse = await fetch(`${CONFIG.API_BASE_URL}/chat/${activeChat.id}/send`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(messageData)
            });
            
            const messageResult = await messageResponse.json();
            
            if (messageResponse.ok) {
                addMessageToUI(messageResult.message);
                showNotification('Image sent successfully', 'success', 1500);
            } else {
                throw new Error(messageResult.error || 'Failed to send image message');
            }
            
        } else {
            throw new Error(data.error || 'Failed to upload image');
        }
        
    } catch (error) {
        console.error('Error uploading image:', error);
        removeImageUploadProgress(messageId);
        showNotification('Failed to upload image', 'error');
    }
}

/**
 * Show image upload progress
 */
function showImageUploadProgress(messageId, file) {
    if (!messageContainer) return;
    
    const progressHtml = `
        <div class="message-bubble own-message upload-progress" data-temp-id="${messageId}">
            <div class="message-content">
                <div class="image-upload-progress">
                    <div class="upload-preview">
                        <img src="${URL.createObjectURL(file)}" alt="Uploading..." class="upload-preview-img">
                        <div class="upload-overlay">
                            <div class="upload-spinner"></div>
                            <span>Uploading...</span>
                        </div>
                    </div>
                    <div class="upload-info">
                        <span class="file-name">${file.name}</span>
                        <span class="file-size">${formatFileSize(file.size)}</span>
                    </div>
                </div>
            </div>
        </div>
    `;
    
    messageContainer.insertAdjacentHTML('beforeend', progressHtml);
    
    if (shouldAutoScroll) {
        setTimeout(scrollToBottom, 100);
    }
}

/**
 * Remove image upload progress
 */
function removeImageUploadProgress(messageId) {
    const progressElement = document.querySelector(`[data-temp-id="${messageId}"]`);
    if (progressElement) {
        progressElement.remove();
    }
}

/**
 * Open image viewer
 */
function openImageViewer(imageUrl, chatId = null) {
    // Collect all images in current chat
    if (chatId && chatId === activeChat?.id) {
        currentImageList = Array.from(document.querySelectorAll('.message-image')).map(img => img.src);
        currentImageIndex = currentImageList.indexOf(imageUrl);
    } else {
        currentImageList = [imageUrl];
        currentImageIndex = 0;
    }
    
    const modalHtml = `
        <div class="modal-overlay image-viewer">
            <div class="image-viewer-modal">
                <div class="image-viewer-content">
                    <img id="viewerImage" src="${imageUrl}" alt="Image">
                    <div class="image-viewer-controls">
                        ${currentImageList.length > 1 ? `
                            <button onclick="previousImage()" class="viewer-btn" title="Previous">⬅️</button>
                            <button onclick="nextImage()" class="viewer-btn" title="Next">➡️</button>
                        ` : ''}
                        <button onclick="downloadImage('${imageUrl}')" class="viewer-btn" title="Download">⬇️</button>
                        <button onclick="closeImageViewer()" class="viewer-btn" title="Close">✖️</button>
                    </div>
                    ${currentImageList.length > 1 ? `
                        <div class="image-counter">
                            <span id="imageCounter">${currentImageIndex + 1} of ${currentImageList.length}</span>
                        </div>
                    ` : ''}
                </div>
            </div>
        </div>
    `;
    
    document.body.insertAdjacentHTML('beforeend', modalHtml);
    setTimeout(() => {
        document.querySelector('.image-viewer').classList.add('show');
        imageViewerOpen = true;
    }, 10);
}

/**
 * Close image viewer
 */
function closeImageViewer() {
    const viewer = document.querySelector('.image-viewer');
    if (viewer) {
        viewer.classList.remove('show');
        setTimeout(() => viewer.remove(), 300);
    }
    imageViewerOpen = false;
}

/**
 * Show next image
 */
function nextImage() {
    if (currentImageIndex < currentImageList.length - 1) {
        currentImageIndex++;
        updateViewerImage();
    }
}

/**
 * Show previous image
 */
function previousImage() {
    if (currentImageIndex > 0) {
        currentImageIndex--;
        updateViewerImage();
    }
}

/**
 * Update viewer image
 */
function updateViewerImage() {
    const viewerImage = document.getElementById('viewerImage');
    const counter = document.getElementById('imageCounter');
    
    if (viewerImage && currentImageList[currentImageIndex]) {
        viewerImage.src = currentImageList[currentImageIndex];
    }
    
    if (counter) {
        counter.textContent = `${currentImageIndex + 1} of ${currentImageList.length}`;
    }
}

/**
 * Setup image viewer keyboard events
 */
function setupImageViewerKeyboardEvents() {
    document.addEventListener('keydown', function(event) {
        if (!imageViewerOpen) return;
        
        switch (event.key) {
            case 'ArrowLeft':
                event.preventDefault();
                previousImage();
                break;
            case 'ArrowRight':
                event.preventDefault();
                nextImage();
                break;
            case 'Escape':
                event.preventDefault();
                closeImageViewer();
                break;
        }
    });
}

/**
 * Download image
 */
function downloadImage(imageUrl) {
    const link = document.createElement('a');
    link.href = imageUrl;
    link.download = 'image-' + Date.now() + '.jpg';
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    
    showNotification('Image download started', 'success', 1500);
}

/**
 * Show/hide image in message
 */
function toggleImageVisibility(imageElement) {
    const messageContent = imageElement.closest('.message-content');
    if (!messageContent) return;
    
    const isHidden = imageElement.style.display === 'none';
    
    if (isHidden) {
        showImageInMessage(imageElement);
    } else {
        hideImageInMessage(imageElement);
    }
}

/**
 * Show image in message
 */
function showImageInMessage(imageElement) {
    imageElement.style.display = 'block';
    
    // Update hide/show button
    const messageContainer = imageElement.closest('.image-message');
    if (messageContainer) {
        let hideBtn = messageContainer.querySelector('.hide-image-btn');
        if (!hideBtn) {
            hideBtn = document.createElement('button');
            hideBtn.className = 'hide-image-btn';
            hideBtn.textContent = 'Hide';
            hideBtn.onclick = () => hideImageInMessage(imageElement);
            messageContainer.appendChild(hideBtn);
        }
        
        // Remove show button
        const showBtn = messageContainer.querySelector('.show-image-btn');
        if (showBtn) {
            showBtn.remove();
        }
    }
}

/**
 * Hide image in message
 */
function hideImageInMessage(imageElement) {
    imageElement.style.display = 'none';
    
    // Update hide/show button
    const messageContainer = imageElement.closest('.image-message');
    if (messageContainer) {
        let showBtn = messageContainer.querySelector('.show-image-btn');
        if (!showBtn) {
            showBtn = document.createElement('button');
            showBtn.className = 'show-image-btn';
            showBtn.textContent = 'Show Image';
            showBtn.onclick = () => showImageInMessage(imageElement);
            messageContainer.appendChild(showBtn);
        }
        
        // Remove hide button
        const hideBtn = messageContainer.querySelector('.hide-image-btn');
        if (hideBtn) {
            hideBtn.remove();
        }
    }
}

/**
 * Setup lazy loading for images
 */
function setupImageLazyLoading() {
    if ('IntersectionObserver' in window) {
        const imageObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    if (img.dataset.src) {
                        img.src = img.dataset.src;
                        img.removeAttribute('data-src');
                        observer.unobserve(img);
                    }
                }
            });
        });
        
        // Observe all images with data-src attribute
        document.querySelectorAll('img[data-src]').forEach(img => {
            imageObserver.observe(img);
        });
    }
}

/**
 * Compress image before upload
 */
function compressImage(file, maxWidth = 1920, maxHeight = 1080, quality = 0.8) {
    return new Promise((resolve) => {
        const canvas = document.createElement('canvas');
        const ctx = canvas.getContext('2d');
        const img = new Image();
        
        img.onload = function() {
            // Calculate new dimensions
            let { width, height } = img;
            
            if (width > maxWidth || height > maxHeight) {
                const ratio = Math.min(maxWidth / width, maxHeight / height);
                width *= ratio;
                height *= ratio;
            }
            
            // Set canvas dimensions
            canvas.width = width;
            canvas.height = height;
            
            // Draw and compress
            ctx.drawImage(img, 0, 0, width, height);
            
            canvas.toBlob((blob) => {
                resolve(blob);
            }, 'image/jpeg', quality);
        };
        
        img.src = URL.createObjectURL(file);
    });
}

/**
 * Validate image file
 */
function validateImageFile(file) {
    const allowedTypes = ['image/jpeg', 'image/jpg', 'image/png', 'image/gif', 'image/webp'];
    const maxSize = 10 * 1024 * 1024; // 10MB
    
    if (!allowedTypes.includes(file.type)) {
        throw new Error('Unsupported image format. Please use JPEG, PNG, GIF, or WebP.');
    }
    
    if (file.size > maxSize) {
        throw new Error('Image is too large. Maximum size is 10MB.');
    }
    
    return true;
}

/**
 * Create image thumbnail
 */
function createImageThumbnail(file, size = 150) {
    return new Promise((resolve) => {
        const canvas = document.createElement('canvas');
        const ctx = canvas.getContext('2d');
        const img = new Image();
        
        img.onload = function() {
            canvas.width = size;
            canvas.height = size;
            
            // Calculate crop area for square thumbnail
            const minDimension = Math.min(img.width, img.height);
            const cropX = (img.width - minDimension) / 2;
            const cropY = (img.height - minDimension) / 2;
            
            ctx.drawImage(img, cropX, cropY, minDimension, minDimension, 0, 0, size, size);
            
            canvas.toBlob((blob) => {
                resolve(URL.createObjectURL(blob));
            }, 'image/jpeg', 0.8);
        };
        
        img.src = URL.createObjectURL(file);
    });
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', initializeImageHandler);

// Export image handler functions
window.ChatApp = {
    ...window.ChatApp,
    openImageViewer,
    closeImageViewer,
    downloadImage,
    toggleImageVisibility,
    compressImage,
    validateImageFile
};

console.log('Image handler module loaded successfully');
