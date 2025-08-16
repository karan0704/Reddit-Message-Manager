import os

def create_util_websocket_and_fragments():
    # Base path from your previous conversation
    base_path = "D:\\Karan Ticket Project\\Reddit Message Manager"

    # Utility classes for the local chat application
    util_files = [
        {
            "path": "src\\main\\java\\com\\anuj\\redditmessagemanager\\util\\DateUtil.java",
            "content": """package com.anuj.redditmessagemanager.util;

import org.springframework.stereotype.Component;

import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.time.temporal.ChronoUnit;

@Component
public class DateUtil {
    
    private static final DateTimeFormatter DEFAULT_FORMATTER = DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss");
    private static final DateTimeFormatter TIME_ONLY_FORMATTER = DateTimeFormatter.ofPattern("HH:mm");
    private static final DateTimeFormatter DATE_ONLY_FORMATTER = DateTimeFormatter.ofPattern("MMM dd, yyyy");
    
    /**
     * Format timestamp for chat message display
     */
    public static String formatMessageTime(LocalDateTime timestamp) {
        if (timestamp == null) {
            return "";
        }
        
        LocalDateTime now = LocalDateTime.now();
        
        // If same day, show time only
        if (timestamp.toLocalDate().equals(now.toLocalDate())) {
            return timestamp.format(TIME_ONLY_FORMATTER);
        }
        
        // If within last 7 days, show day and time
        if (ChronoUnit.DAYS.between(timestamp, now) <= 7) {
            return timestamp.format(DateTimeFormatter.ofPattern("EEE HH:mm"));
        }
        
        // Otherwise show full date
        return timestamp.format(DATE_ONLY_FORMATTER);
    }
    
    /**
     * Format timestamp for detailed display
     */
    public static String formatDetailedTime(LocalDateTime timestamp) {
        if (timestamp == null) {
            return "Unknown time";
        }
        
        return timestamp.format(DEFAULT_FORMATTER);
    }
    
    /**
     * Get relative time (e.g., "2 minutes ago")
     */
    public static String getRelativeTime(LocalDateTime timestamp) {
        if (timestamp == null) {
            return "Unknown time";
        }
        
        LocalDateTime now = LocalDateTime.now();
        long minutes = ChronoUnit.MINUTES.between(timestamp, now);
        long hours = ChronoUnit.HOURS.between(timestamp, now);
        long days = ChronoUnit.DAYS.between(timestamp, now);
        
        if (minutes < 1) {
            return "Just now";
        } else if (minutes < 60) {
            return minutes + " minute" + (minutes > 1 ? "s" : "") + " ago";
        } else if (hours < 24) {
            return hours + " hour" + (hours > 1 ? "s" : "") + " ago";
        } else if (days < 7) {
            return days + " day" + (days > 1 ? "s" : "") + " ago";
        } else {
            return formatDetailedTime(timestamp);
        }
    }
    
    /**
     * Check if timestamp is today
     */
    public static boolean isToday(LocalDateTime timestamp) {
        if (timestamp == null) {
            return false;
        }
        
        return timestamp.toLocalDate().equals(LocalDateTime.now().toLocalDate());
    }
    
    /**
     * Check if timestamp is this week
     */
    public static boolean isThisWeek(LocalDateTime timestamp) {
        if (timestamp == null) {
            return false;
        }
        
        return ChronoUnit.DAYS.between(timestamp, LocalDateTime.now()) <= 7;
    }
}
"""
        },

        {
            "path": "src\\main\\java\\com\\anuj\\redditmessagemanager\\util\\FileUtil.java",
            "content": """package com.anuj.redditmessagemanager.util;

import org.springframework.stereotype.Component;
import org.springframework.web.multipart.MultipartFile;

import java.io.File;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.UUID;

@Component
public class FileUtil {
    
    private static final String UPLOAD_DIR = "./uploads/";
    private static final long MAX_FILE_SIZE = 10 * 1024 * 1024; // 10MB
    private static final String[] ALLOWED_IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".webp"};
    private static final String[] ALLOWED_FILE_EXTENSIONS = {".pdf", ".doc", ".docx", ".txt", ".zip"};
    
    /**
     * Save uploaded file
     */
    public static String saveFile(MultipartFile file, String directory) throws IOException {
        if (file.isEmpty()) {
            throw new IOException("File is empty");
        }
        
        if (file.getSize() > MAX_FILE_SIZE) {
            throw new IOException("File size exceeds maximum limit");
        }
        
        // Create directory if it doesn't exist
        Path uploadPath = Paths.get(UPLOAD_DIR + directory);
        Files.createDirectories(uploadPath);
        
        // Generate unique filename
        String originalFilename = file.getOriginalFilename();
        String extension = getFileExtension(originalFilename);
        String uniqueFilename = UUID.randomUUID().toString() + extension;
        
        // Save file
        Path filePath = uploadPath.resolve(uniqueFilename);
        Files.copy(file.getInputStream(), filePath);
        
        return directory + "/" + uniqueFilename;
    }
    
    /**
     * Get file extension
     */
    public static String getFileExtension(String filename) {
        if (filename == null || filename.isEmpty()) {
            return "";
        }
        
        int lastDot = filename.lastIndexOf('.');
        return lastDot > 0 ? filename.substring(lastDot).toLowerCase() : "";
    }
    
    /**
     * Check if file is an image
     */
    public static boolean isImageFile(String filename) {
        String extension = getFileExtension(filename);
        
        for (String allowedExt : ALLOWED_IMAGE_EXTENSIONS) {
            if (allowedExt.equals(extension)) {
                return true;
            }
        }
        
        return false;
    }
    
    /**
     * Check if file type is allowed
     */
    public static boolean isAllowedFileType(String filename) {
        String extension = getFileExtension(filename);
        
        // Check images
        for (String allowedExt : ALLOWED_IMAGE_EXTENSIONS) {
            if (allowedExt.equals(extension)) {
                return true;
            }
        }
        
        // Check other files
        for (String allowedExt : ALLOWED_FILE_EXTENSIONS) {
            if (allowedExt.equals(extension)) {
                return true;
            }
        }
        
        return false;
    }
    
    /**
     * Format file size for display
     */
    public static String formatFileSize(long bytes) {
        if (bytes < 1024) {
            return bytes + " B";
        } else if (bytes < 1024 * 1024) {
            return String.format("%.1f KB", bytes / 1024.0);
        } else if (bytes < 1024 * 1024 * 1024) {
            return String.format("%.1f MB", bytes / (1024.0 * 1024.0));
        } else {
            return String.format("%.1f GB", bytes / (1024.0 * 1024.0 * 1024.0));
        }
    }
    
    /**
     * Delete file
     */
    public static boolean deleteFile(String filePath) {
        try {
            Path path = Paths.get(UPLOAD_DIR + filePath);
            return Files.deleteIfExists(path);
        } catch (IOException e) {
            return false;
        }
    }
    
    /**
     * Check if file exists
     */
    public static boolean fileExists(String filePath) {
        Path path = Paths.get(UPLOAD_DIR + filePath);
        return Files.exists(path);
    }
}
"""
        },

        {
            "path": "src\\main\\java\\com\\anuj\\redditmessagemanager\\util\\ImageUtil.java",
            "content": """package com.anuj.redditmessagemanager.util;

import org.springframework.stereotype.Component;

import javax.imageio.ImageIO;
import java.awt.*;
import java.awt.image.BufferedImage;
import java.io.File;
import java.io.IOException;

@Component
public class ImageUtil {
    
    private static final int THUMBNAIL_SIZE = 150;
    private static final int MAX_IMAGE_WIDTH = 1920;
    private static final int MAX_IMAGE_HEIGHT = 1080;
    
    /**
     * Create thumbnail of image
     */
    public static String createThumbnail(String imagePath) throws IOException {
        File originalFile = new File("./uploads/" + imagePath);
        if (!originalFile.exists()) {
            throw new IOException("Original image not found");
        }
        
        BufferedImage originalImage = ImageIO.read(originalFile);
        if (originalImage == null) {
            throw new IOException("Cannot read image file");
        }
        
        // Calculate thumbnail dimensions
        int width = originalImage.getWidth();
        int height = originalImage.getHeight();
        
        double scale = Math.min((double) THUMBNAIL_SIZE / width, (double) THUMBNAIL_SIZE / height);
        int thumbnailWidth = (int) (width * scale);
        int thumbnailHeight = (int) (height * scale);
        
        // Create thumbnail
        BufferedImage thumbnail = new BufferedImage(thumbnailWidth, thumbnailHeight, BufferedImage.TYPE_INT_RGB);
        Graphics2D g2d = thumbnail.createGraphics();
        g2d.setRenderingHint(RenderingHints.KEY_INTERPOLATION, RenderingHints.VALUE_INTERPOLATION_BILINEAR);
        g2d.drawImage(originalImage, 0, 0, thumbnailWidth, thumbnailHeight, null);
        g2d.dispose();
        
        // Save thumbnail
        String thumbnailPath = imagePath.replace(".", "_thumb.");
        File thumbnailFile = new File("./uploads/" + thumbnailPath);
        ImageIO.write(thumbnail, "jpg", thumbnailFile);
        
        return thumbnailPath;
    }
    
    /**
     * Resize image if too large
     */
    public static String resizeIfNeeded(String imagePath) throws IOException {
        File originalFile = new File("./uploads/" + imagePath);
        BufferedImage originalImage = ImageIO.read(originalFile);
        
        if (originalImage == null) {
            return imagePath;
        }
        
        int width = originalImage.getWidth();
        int height = originalImage.getHeight();
        
        // Check if resize is needed
        if (width <= MAX_IMAGE_WIDTH && height <= MAX_IMAGE_HEIGHT) {
            return imagePath;
        }
        
        // Calculate new dimensions
        double scale = Math.min((double) MAX_IMAGE_WIDTH / width, (double) MAX_IMAGE_HEIGHT / height);
        int newWidth = (int) (width * scale);
        int newHeight = (int) (height * scale);
        
        // Resize image
        BufferedImage resizedImage = new BufferedImage(newWidth, newHeight, BufferedImage.TYPE_INT_RGB);
        Graphics2D g2d = resizedImage.createGraphics();
        g2d.setRenderingHint(RenderingHints.KEY_INTERPOLATION, RenderingHints.VALUE_INTERPOLATION_BILINEAR);
        g2d.drawImage(originalImage, 0, 0, newWidth, newHeight, null);
        g2d.dispose();
        
        // Save resized image
        String resizedPath = imagePath.replace(".", "_resized.");
        File resizedFile = new File("./uploads/" + resizedPath);
        ImageIO.write(resizedImage, "jpg", resizedFile);
        
        // Delete original if different
        if (!resizedPath.equals(imagePath)) {
            originalFile.delete();
        }
        
        return resizedPath;
    }
    
    /**
     * Get image dimensions
     */
    public static Dimension getImageDimensions(String imagePath) throws IOException {
        File imageFile = new File("./uploads/" + imagePath);
        BufferedImage image = ImageIO.read(imageFile);
        
        if (image == null) {
            throw new IOException("Cannot read image file");
        }
        
        return new Dimension(image.getWidth(), image.getHeight());
    }
    
    /**
     * Check if image is valid
     */
    public static boolean isValidImage(String imagePath) {
        try {
            File imageFile = new File("./uploads/" + imagePath);
            BufferedImage image = ImageIO.read(imageFile);
            return image != null;
        } catch (IOException e) {
            return false;
        }
    }
}
"""
        }
    ]

    # WebSocket classes
    websocket_files = [
        {
            "path": "src\\main\\java\\com\\anuj\\redditmessagemanager\\websocket\\ChatWebSocketHandler.java",
            "content": """package com.anuj.redditmessagemanager.websocket;

import com.anuj.redditmessagemanager.dto.MessageDto;
import com.anuj.redditmessagemanager.entity.Message.MessageType;
import com.anuj.redditmessagemanager.service.MessageService;
import com.anuj.redditmessagemanager.service.ChatService;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;
import org.springframework.web.socket.*;

import java.io.IOException;
import java.util.Map;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.CopyOnWriteArraySet;

@Component
public class ChatWebSocketHandler implements WebSocketHandler {
    
    private static final Logger logger = LoggerFactory.getLogger(ChatWebSocketHandler.class);
    
    @Autowired
    private MessageService messageService;
    
    @Autowired
    private ChatService chatService;
    
    @Autowired
    private ObjectMapper objectMapper;
    
    // Store active sessions by username
    private final Map<String, WebSocketSession> userSessions = new ConcurrentHashMap<>();
    
    // Store all active sessions
    private final CopyOnWriteArraySet<WebSocketSession> activeSessions = new CopyOnWriteArraySet<>();
    
    @Override
    public void afterConnectionEstablished(WebSocketSession session) throws Exception {
        activeSessions.add(session);
        
        String username = getUsernameFromSession(session);
        if (username != null) {
            userSessions.put(username, session);
            logger.info("WebSocket connection established for user: {}", username);
            
            // Send connection confirmation
            sendMessage(session, Map.of(
                "type", "connection",
                "status", "connected",
                "message", "WebSocket connection established"
            ));
        } else {
            logger.warn("WebSocket connection established without valid username");
        }
    }
    
    @Override
    public void handleMessage(WebSocketSession session, WebSocketMessage<?> message) throws Exception {
        try {
            String payload = message.getPayload().toString();
            Map<String, Object> messageData = objectMapper.readValue(payload, Map.class);
            
            String messageType = (String) messageData.get("type");
            String username = getUsernameFromSession(session);
            
            if (username == null) {
                sendError(session, "User not authenticated");
                return;
            }
            
            switch (messageType) {
                case "chat_message":
                    handleChatMessage(session, messageData, username);
                    break;
                    
                case "typing":
                    handleTypingIndicator(session, messageData, username);
                    break;
                    
                case "join_chat":
                    handleJoinChat(session, messageData, username);
                    break;
                    
                case "leave_chat":
                    handleLeaveChat(session, messageData, username);
                    break;
                    
                case "ping":
                    handlePing(session);
                    break;
                    
                default:
                    logger.warn("Unknown message type: {}", messageType);
                    sendError(session, "Unknown message type");
            }
            
        } catch (Exception e) {
            logger.error("Error handling WebSocket message: {}", e.getMessage());
            sendError(session, "Error processing message");
        }
    }
    
    @Override
    public void handleTransportError(WebSocketSession session, Throwable exception) throws Exception {
        logger.error("WebSocket transport error: {}", exception.getMessage());
        cleanupSession(session);
    }
    
    @Override
    public void afterConnectionClosed(WebSocketSession session, CloseStatus closeStatus) throws Exception {
        cleanupSession(session);
        logger.info("WebSocket connection closed with status: {}", closeStatus);
    }
    
    @Override
    public boolean supportsPartialMessages() {
        return false;
    }
    
    /**
     * Handle chat message
     */
    private void handleChatMessage(WebSocketSession session, Map<String, Object> messageData, String username) {
        try {
            Long chatId = Long.valueOf(messageData.get("chatId").toString());
            String content = (String) messageData.get("content");
            String messageTypeStr = (String) messageData.getOrDefault("messageType", "TEXT");
            
            // Create message DTO
            MessageDto messageDto = new MessageDto();
            messageDto.setMessageContent(content);
            messageDto.setMessageType(MessageType.valueOf(messageTypeStr));
            
            // Save message
            MessageDto savedMessage = messageService.sendMessage(chatId, username, messageDto);
            
            // Send confirmation to sender
            sendMessage(session, Map.of(
                "type", "message_sent",
                "message", savedMessage
            ));
            
            // Broadcast to other participants in the chat
            broadcastToChat(chatId, username, Map.of(
                "type", "new_message",
                "message", savedMessage
            ));
            
        } catch (Exception e) {
            logger.error("Error handling chat message: {}", e.getMessage());
            sendError(session, "Failed to send message");
        }
    }
    
    /**
     * Handle typing indicator
     */
    private void handleTypingIndicator(WebSocketSession session, Map<String, Object> messageData, String username) {
        try {
            Long chatId = Long.valueOf(messageData.get("chatId").toString());
            Boolean isTyping = (Boolean) messageData.getOrDefault("isTyping", false);
            
            // Broadcast typing indicator to other participants
            broadcastToChat(chatId, username, Map.of(
                "type", "typing",
                "username", username,
                "isTyping", isTyping,
                "chatId", chatId
            ));
            
        } catch (Exception e) {
            logger.error("Error handling typing indicator: {}", e.getMessage());
        }
    }
    
    /**
     * Handle join chat
     */
    private void handleJoinChat(WebSocketSession session, Map<String, Object> messageData, String username) {
        try {
            Long chatId = Long.valueOf(messageData.get("chatId").toString());
            
            // Store chat ID in session attributes
            session.getAttributes().put("chatId", chatId);
            
            // Send confirmation
            sendMessage(session, Map.of(
                "type", "chat_joined",
                "chatId", chatId
            ));
            
            // Notify other participants
            broadcastToChat(chatId, username, Map.of(
                "type", "user_joined",
                "username", username,
                "chatId", chatId
            ));
            
        } catch (Exception e) {
            logger.error("Error handling join chat: {}", e.getMessage());
            sendError(session, "Failed to join chat");
        }
    }
    
    /**
     * Handle leave chat
     */
    private void handleLeaveChat(WebSocketSession session, Map<String, Object> messageData, String username) {
        try {
            Long chatId = Long.valueOf(messageData.get("chatId").toString());
            
            // Remove chat ID from session attributes
            session.getAttributes().remove("chatId");
            
            // Send confirmation
            sendMessage(session, Map.of(
                "type", "chat_left",
                "chatId", chatId
            ));
            
            // Notify other participants
            broadcastToChat(chatId, username, Map.of(
                "type", "user_left",
                "username", username,
                "chatId", chatId
            ));
            
        } catch (Exception e) {
            logger.error("Error handling leave chat: {}", e.getMessage());
        }
    }
    
    /**
     * Handle ping message
     */
    private void handlePing(WebSocketSession session) {
        sendMessage(session, Map.of(
            "type", "pong",
            "timestamp", System.currentTimeMillis()
        ));
    }
    
    /**
     * Send message to WebSocket session
     */
    private void sendMessage(WebSocketSession session, Object message) {
        try {
            if (session.isOpen()) {
                String jsonMessage = objectMapper.writeValueAsString(message);
                session.sendMessage(new TextMessage(jsonMessage));
            }
        } catch (IOException e) {
            logger.error("Error sending WebSocket message: {}", e.getMessage());
        }
    }
    
    /**
     * Send error message
     */
    private void sendError(WebSocketSession session, String errorMessage) {
        sendMessage(session, Map.of(
            "type", "error",
            "message", errorMessage
        ));
    }
    
    /**
     * Broadcast message to all participants in a chat
     */
    private void broadcastToChat(Long chatId, String senderUsername, Object message) {
        for (Map.Entry<String, WebSocketSession> entry : userSessions.entrySet()) {
            String username = entry.getKey();
            WebSocketSession session = entry.getValue();
            
            // Don't send to sender
            if (username.equals(senderUsername)) {
                continue;
            }
            
            // Check if user is in the chat (simplified check)
            Long userChatId = (Long) session.getAttributes().get("chatId");
            if (chatId.equals(userChatId)) {
                sendMessage(session, message);
            }
        }
    }
    
    /**
     * Get username from session
     */
    private String getUsernameFromSession(WebSocketSession session) {
        // In a real application, you'd get this from the session or JWT token
        // For now, we'll try to get it from session attributes or headers
        Object username = session.getAttributes().get("username");
        if (username != null) {
            return username.toString();
        }
        
        // Try to get from handshake headers or query parameters
        String query = session.getUri().getQuery();
        if (query != null && query.contains("username=")) {
            String[] params = query.split("&");
            for (String param : params) {
                if (param.startsWith("username=")) {
                    return param.substring(9); // Remove "username="
                }
            }
        }
        
        return null;
    }
    
    /**
     * Cleanup session
     */
    private void cleanupSession(WebSocketSession session) {
        activeSessions.remove(session);
        
        String username = getUsernameFromSession(session);
        if (username != null) {
            userSessions.remove(username);
            logger.info("Cleaned up WebSocket session for user: {}", username);
        }
    }
    
    /**
     * Send message to specific user
     */
    public void sendMessageToUser(String username, Object message) {
        WebSocketSession session = userSessions.get(username);
        if (session != null && session.isOpen()) {
            sendMessage(session, message);
        }
    }
    
    /**
     * Get active users count
     */
    public int getActiveUsersCount() {
        return userSessions.size();
    }
    
    /**
     * Check if user is online
     */
    public boolean isUserOnline(String username) {
        WebSocketSession session = userSessions.get(username);
        return session != null && session.isOpen();
    }
}
"""
        }
    ]

    # Thymeleaf fragments
    fragment_files = [
        {
            "path": "src\\main\\resources\\templates\\fragments\\sidebar.html",
            "content": """<!DOCTYPE html>
<html lang="en" xmlns:th="http://www.thymeleaf.org">
<head>
    <meta charset="UTF-8">
    <title>Chat Sidebar</title>
</head>
<body>
    <!-- Chat Sidebar Fragment -->
    <div th:fragment="sidebar" class="chat-sidebar">
        <div class="sidebar-header">
            <h3>Chats</h3>
            <div class="sidebar-actions">
                <button id="bulkSelectBtn" class="bulk-select-btn" onclick="toggleBulkMode()">
                    <i class="icon-select"></i> Select
                </button>
                <button class="new-chat-btn" onclick="showNewChatModal()">
                    <i class="icon-plus"></i>
                </button>
            </div>
        </div>
        
        <!-- Search Bar -->
        <div class="search-container">
            <input type="text" id="chatSearch" placeholder="Search chats..." class="search-input" onkeyup="filterChats()">
            <button class="search-btn" onclick="searchChats()">
                <i class="icon-search"></i>
            </button>
        </div>
        
        <!-- Filter Options -->
        <div class="filter-options">
            <button class="filter-btn active" data-filter="all" onclick="filterChatsByType('all')">All</button>
            <button class="filter-btn" data-filter="unread" onclick="filterChatsByType('unread')">Unread</button>
            <button class="filter-btn" data-filter="pinned" onclick="filterChatsByType('pinned')">Pinned</button>
        </div>
        
        <!-- Chat List -->
        <div id="chatList" class="chat-list">
            <div class="loading" id="chatLoading">
                <div class="spinner"></div>
                <span>Loading chats...</span>
            </div>
        </div>
        
        <!-- Bulk Actions (Hidden by default) -->
        <div id="bulkActions" class="bulk-actions hidden">
            <button onclick="bulkDeleteChats()" class="btn btn-danger">
                <i class="icon-delete"></i> Delete Selected
            </button>
            <button onclick="bulkPinChats()" class="btn btn-primary">
                <i class="icon-pin"></i> Pin Selected
            </button>
            <button onclick="bulkBlockUsers()" class="btn btn-warning">
                <i class="icon-block"></i> Block Selected
            </button>
            <button onclick="cancelBulkMode()" class="btn btn-secondary">
                <i class="icon-cancel"></i> Cancel
            </button>
        </div>
    </div>
    
    <!-- Chat List Item Template -->
    <div th:fragment="chat-item" class="chat-item" th:data-chat-id="${chat.id}">
        <div class="chat-avatar">
            <img th:src="${chat.otherUsername != null ? '/api/user/' + chat.otherUsername + '/avatar' : '/images/default-avatar.png'}" 
                 th:alt="${chat.otherUsername}" class="avatar-img">
            <div th:if="${chat.hasUnread}" class="unread-indicator"></div>
        </div>
        
        <div class="chat-content">
            <div class="chat-header">
                <span class="chat-username" th:text="${chat.otherUsername}">Username</span>
                <span class="chat-time" th:text="${#temporals.format(chat.lastMessageTimestamp, 'HH:mm')}">12:30</span>
            </div>
            
            <div class="chat-preview">
                <span class="last-message" th:text="${chat.lastMessage}">Last message preview...</span>
                <div class="chat-indicators">
                    <span th:if="${chat.isPinned}" class="pinned-indicator" title="Pinned">📌</span>
                    <span th:if="${chat.hasUnread and chat.unreadCount > 0}" 
                          class="unread-count" th:text="${chat.unreadCount}">3</span>
                </div>
            </div>
        </div>
        
        <div class="chat-actions">
            <button class="pin-btn" th:onclick="'togglePin(' + ${chat.id} + ')'" 
                    th:title="${chat.isPinned} ? 'Unpin' : 'Pin'">
                <i th:class="${chat.isPinned} ? 'icon-pin-filled' : 'icon-pin'"></i>
            </button>
            <div class="chat-checkbox">
                <input type="checkbox" th:id="'chat-' + ${chat.id}" class="chat-select-checkbox">
            </div>
        </div>
    </div>
</body>
</html>
"""
        },

        {
            "path": "src\\main\\resources\\templates\\fragments\\message-bubble.html",
            "content": """<!DOCTYPE html>
<html lang="en" xmlns:th="http://www.thymeleaf.org">
<head>
    <meta charset="UTF-8">
    <title>Message Bubble</title>
</head>
<body>
    <!-- Message Bubble Fragment -->
    <div th:fragment="message-bubble" class="message-bubble" 
         th:classappend="${message.isOwnMessage} ? 'own-message' : 'other-message'"
         th:data-message-id="${message.id}">
        
        <!-- Message Header (for other user's messages) -->
        <div th:if="${!message.isOwnMessage}" class="message-header">
            <span class="sender-name" th:text="${message.senderUsername}">Sender</span>
            <span class="message-time" th:text="${message.formattedTime}">12:30</span>
        </div>
        
        <!-- Message Content -->
        <div class="message-content">
            <!-- Text Message -->
            <div th:if="${message.messageType.name() == 'TEXT'}" class="text-message">
                <p th:text="${message.messageContent}">Message content here...</p>
            </div>
            
            <!-- Image Message -->
            <div th:if="${message.messageType.name() == 'IMAGE'}" class="image-message">
                <div th:if="${message.isImageHidden}" class="image-hidden">
                    <i class="icon-image"></i>
                    <span>Image hidden</span>
                    <button onclick="showImage(this)" class="show-image-btn">Show</button>
                </div>
                <div th:unless="${message.isImageHidden}" class="image-visible">
                    <img th:src="${message.imageUrl}" th:alt="'Image from ' + ${message.senderUsername}" class="message-image">
                    <button onclick="hideImage(this)" class="hide-image-btn">Hide</button>
                </div>
            </div>
            
            <!-- File Message -->
            <div th:if="${message.messageType.name() == 'FILE'}" class="file-message">
                <div class="file-info">
                    <i class="icon-file"></i>
                    <div class="file-details">
                        <span class="file-name" th:text="${message.fileName}">document.pdf</span>
                        <span class="file-size" th:text="${message.fileSize != null ? #numbers.formatDecimal(message.fileSize / 1024, 1, 1) + ' KB' : ''}">1.2 KB</span>
                    </div>
                    <a th:href="${message.fileUrl}" class="download-btn" download>
                        <i class="icon-download"></i>
                    </a>
                </div>
            </div>
            
            <!-- System Message -->
            <div th:if="${message.messageType.name() == 'SYSTEM'}" class="system-message">
                <i class="icon-info"></i>
                <span th:text="${message.messageContent}">System message</span>
            </div>
        </div>
        
        <!-- Message Footer (for own messages) -->
        <div th:if="${message.isOwnMessage}" class="message-footer">
            <span class="message-time" th:text="${message.formattedTime}">12:30</span>
            <span th:if="${message.isRead}" class="read-indicator" title="Read">✓✓</span>
            <span th:unless="${message.isRead}" class="sent-indicator" title="Sent">✓</span>
        </div>
        
        <!-- Message Actions -->
        <div class="message-actions">
            <button class="reply-btn" th:onclick="'replyToMessage(' + ${message.id} + ')'" title="Reply">
                <i class="icon-reply"></i>
            </button>
            <button th:if="${message.isOwnMessage}" class="delete-btn" 
                    th:onclick="'deleteMessage(' + ${message.id} + ')'" title="Delete">
                <i class="icon-delete"></i>
            </button>
            <button class="copy-btn" th:onclick="'copyMessage(' + ${message.id} + ')'" title="Copy">
                <i class="icon-copy"></i>
            </button>
        </div>
    </div>
    
    <!-- Typing Indicator Fragment -->
    <div th:fragment="typing-indicator" class="typing-indicator" id="typingIndicator">
        <div class="typing-avatar">
            <img src="/images/default-avatar.png" alt="User" class="avatar-img">
        </div>
        <div class="typing-content">
            <span class="typing-user">Someone</span>
            <span class="typing-text">is typing</span>
            <div class="typing-dots">
                <span></span>
                <span></span>
                <span></span>
            </div>
        </div>
    </div>
</body>
</html>
"""
        },

        {
            "path": "src\\main\\resources\\templates\\fragments\\search-bar.html",
            "content": """<!DOCTYPE html>
<html lang="en" xmlns:th="http://www.thymeleaf.org">
<head>
    <meta charset="UTF-8">
    <title>Search Bar</title>
</head>
<body>
    <!-- Search Bar Fragment -->
    <div th:fragment="search-bar" class="search-bar-container">
        <div class="search-main">
            <div class="search-input-container">
                <input type="text" id="mainSearchInput" placeholder="Search chats, users, or messages..." 
                       class="main-search-input" onkeyup="handleSearchInput(event)">
                <button class="search-btn" onclick="performSearch()">
                    <i class="icon-search"></i>
                </button>
                <button class="filter-toggle-btn" onclick="toggleFilters()">
                    <i class="icon-filter"></i>
                </button>
            </div>
            
            <!-- Search Suggestions -->
            <div id="searchSuggestions" class="search-suggestions hidden">
                <!-- Dynamic suggestions will be populated here -->
            </div>
        </div>
        
        <!-- Advanced Filters Panel -->
        <div id="filtersPanel" class="filters-panel hidden">
            <div class="filter-row">
                <label for="searchType">Search in:</label>
                <select id="searchType" class="filter-select">
                    <option value="all">Everything</option>
                    <option value="messages">Messages</option>
                    <option value="users">Users</option>
                    <option value="chats">Chats</option>
                </select>
            </div>
            
            <div class="filter-row">
                <label for="dateFrom">From date:</label>
                <input type="date" id="dateFrom" class="filter-input">
            </div>
            
            <div class="filter-row">
                <label for="dateTo">To date:</label>
                <input type="date" id="dateTo" class="filter-input">
            </div>
            
            <div class="filter-row">
                <label for="userFilter">User:</label>
                <input type="text" id="userFilter" placeholder="Username..." class="filter-input">
            </div>
            
            <div class="filter-row">
                <label class="checkbox-label">
                    <input type="checkbox" id="onlyUnread">
                    <span class="checkmark"></span>
                    Only unread messages
                </label>
            </div>
            
            <div class="filter-row">
                <label class="checkbox-label">
                    <input type="checkbox" id="onlyPinned">
                    <span class="checkmark"></span>
                    Only pinned chats
                </label>
            </div>
            
            <div class="filter-actions">
                <button onclick="applyFilters()" class="btn btn-primary">Apply Filters</button>
                <button onclick="clearFilters()" class="btn btn-secondary">Clear</button>
            </div>
        </div>
        
        <!-- Search Results Preview -->
        <div id="searchResults" class="search-results hidden">
            <div class="results-header">
                <h4>Search Results</h4>
                <button onclick="closeSearchResults()" class="close-btn">×</button>
            </div>
            <div id="searchResultsContent" class="results-content">
                <!-- Dynamic search results -->
            </div>
        </div>
    </div>
    
    <!-- Search Result Item Fragment -->
    <div th:fragment="search-result-item" class="search-result-item" th:data-result-type="${result.type}">
        <!-- Message Result -->
        <div th:if="${result.type == 'message'}" class="message-result">
            <div class="result-icon">
                <i class="icon-message"></i>
            </div>
            <div class="result-content">
                <div class="result-title" th:text="${result.title}">Message from User</div>
                <div class="result-preview" th:text="${result.preview}">Message preview...</div>
                <div class="result-meta">
                    <span th:text="${result.date}">2 days ago</span> • 
                    <span th:text="${result.chat}">Chat with John</span>
                </div>
            </div>
        </div>
        
        <!-- User Result -->
        <div th:if="${result.type == 'user'}" class="user-result">
            <div class="result-avatar">
                <img th:src="${result.avatar}" th:alt="${result.username}" class="avatar-img">
            </div>
            <div class="result-content">
                <div class="result-title" th:text="${result.displayName}">John Doe</div>
                <div class="result-subtitle" th:text="'@' + ${result.username}">@johndoe</div>
                <div class="result-meta">
                    <span th:if="${result.isOnline}" class="online-status">Online</span>
                    <span th:unless="${result.isOnline}" class="offline-status">Offline</span>
                </div>
            </div>
            <div class="result-actions">
                <button th:onclick="'startChat(\\'' + ${result.username} + '\\')'" class="btn btn-small btn-primary">
                    Chat
                </button>
            </div>
        </div>
        
        <!-- Chat Result -->
        <div th:if="${result.type == 'chat'}" class="chat-result">
            <div class="result-icon">
                <i class="icon-chat"></i>
            </div>
            <div class="result-content">
                <div class="result-title" th:text="${result.title}">Chat with User</div>
                <div class="result-preview" th:text="${result.lastMessage}">Last message...</div>
                <div class="result-meta">
                    <span th:text="${result.messageCount} + ' messages'">15 messages</span> • 
                    <span th:text="${result.lastActivity}">3 hours ago</span>
                </div>
            </div>
        </div>
    </div>
</body>
</html>
"""
        },

        {
            "path": "src\\main\\resources\\templates\\fragments\\filter-panel.html",
            "content": """<!DOCTYPE html>
<html lang="en" xmlns:th="http://www.thymeleaf.org">
<head>
    <meta charset="UTF-8">
    <title>Filter Panel</title>
</head>
<body>
    <!-- Filter Panel Fragment -->
    <div th:fragment="filter-panel" class="filter-panel" id="filterPanel">
        <div class="filter-header">
            <h4>Filters</h4>
            <button onclick="closeFilters()" class="close-btn">×</button>
        </div>
        
        <div class="filter-content">
            <!-- Date Range Filter -->
            <div class="filter-section">
                <h5>Date Range</h5>
                <div class="date-range">
                    <div class="date-input-group">
                        <label for="filterDateFrom">From:</label>
                        <input type="date" id="filterDateFrom" class="date-input">
                    </div>
                    <div class="date-input-group">
                        <label for="filterDateTo">To:</label>
                        <input type="date" id="filterDateTo" class="date-input">
                    </div>
                </div>
                <div class="quick-date-filters">
                    <button onclick="setDateRange('today')" class="quick-filter-btn">Today</button>
                    <button onclick="setDateRange('week')" class="quick-filter-btn">This Week</button>
                    <button onclick="setDateRange('month')" class="quick-filter-btn">This Month</button>
                </div>
            </div>
            
            <!-- User Filter -->
            <div class="filter-section">
                <h5>Users</h5>
                <div class="user-filter">
                    <input type="text" id="userFilterInput" placeholder="Search users..." 
                           class="filter-input" onkeyup="searchUsers(this.value)">
                    <div id="userSuggestions" class="user-suggestions hidden">
                        <!-- Dynamic user suggestions -->
                    </div>
                </div>
                <div class="selected-users" id="selectedUsers">
                    <!-- Selected users will appear here -->
                </div>
            </div>
            
            <!-- Message Type Filter -->
            <div class="filter-section">
                <h5>Message Types</h5>
                <div class="checkbox-group">
                    <label class="checkbox-label">
                        <input type="checkbox" id="filterText" checked>
                        <span class="checkmark"></span>
                        <i class="icon-text"></i> Text Messages
                    </label>
                    <label class="checkbox-label">
                        <input type="checkbox" id="filterImages" checked>
                        <span class="checkmark"></span>
                        <i class="icon-image"></i> Images
                    </label>
                    <label class="checkbox-label">
                        <input type="checkbox" id="filterFiles" checked>
                        <span class="checkmark"></span>
                        <i class="icon-file"></i> Files
                    </label>
                    <label class="checkbox-label">
                        <input type="checkbox" id="filterSystem">
                        <span class="checkmark"></span>
                        <i class="icon-system"></i> System Messages
                    </label>
                </div>
            </div>
            
            <!-- Status Filter -->
            <div class="filter-section">
                <h5>Status</h5>
                <div class="radio-group">
                    <label class="radio-label">
                        <input type="radio" name="statusFilter" value="all" checked>
                        <span class="radio-checkmark"></span>
                        All Messages
                    </label>
                    <label class="radio-label">
                        <input type="radio" name="statusFilter" value="read">
                        <span class="radio-checkmark"></span>
                        Read Only
                    </label>
                    <label class="radio-label">
                        <input type="radio" name="statusFilter" value="unread">
                        <span class="radio-checkmark"></span>
                        Unread Only
                    </label>
                </div>
            </div>
            
            <!-- Chat Status Filter -->
            <div class="filter-section">
                <h5>Chat Status</h5>
                <div class="checkbox-group">
                    <label class="checkbox-label">
                        <input type="checkbox" id="filterPinned">
                        <span class="checkmark"></span>
                        <i class="icon-pin"></i> Pinned Chats Only
                    </label>
                    <label class="checkbox-label">
                        <input type="checkbox" id="filterArchived">
                        <span class="checkmark"></span>
                        <i class="icon-archive"></i> Include Archived
                    </label>
                </div>
            </div>
            
            <!-- Sort Options -->
            <div class="filter-section">
                <h5>Sort By</h5>
                <select id="sortBy" class="filter-select">
                    <option value="recent">Most Recent</option>
                    <option value="oldest">Oldest First</option>
                    <option value="username">Username A-Z</option>
                    <option value="username_desc">Username Z-A</option>
                    <option value="message_count">Message Count</option>
                </select>
            </div>
        </div>
        
        <!-- Filter Actions -->
        <div class="filter-actions">
            <button onclick="applyAdvancedFilters()" class="btn btn-primary">Apply Filters</button>
            <button onclick="resetFilters()" class="btn btn-secondary">Reset</button>
            <button onclick="saveFilterPreset()" class="btn btn-outline">Save Preset</button>
        </div>
        
        <!-- Filter Presets -->
        <div class="filter-presets">
            <h5>Quick Presets</h5>
            <div class="preset-buttons">
                <button onclick="loadPreset('unread_today')" class="preset-btn">Unread Today</button>
                <button onclick="loadPreset('images_week')" class="preset-btn">Images This Week</button>
                <button onclick="loadPreset('important')" class="preset-btn">Important Chats</button>
            </div>
        </div>
    </div>
    
    <!-- Selected User Tag Fragment -->
    <div th:fragment="user-tag" class="user-tag" th:data-username="${username}">
        <span class="user-tag-name" th:text="${displayName}">John Doe</span>
        <button onclick="removeUserFilter(this)" class="remove-tag-btn">×</button>
    </div>
</body>
</html>
"""
        }
    ]

    # Function to create files
    def create_files(files_list, file_type):
        print(f"\nCreating {file_type} files...")

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

    # Create all files
    create_files(util_files, "Utility")
    create_files(websocket_files, "WebSocket")
    create_files(fragment_files, "Thymeleaf Fragment")

    print("\n" + "="*70)
    print("Utility, WebSocket, and Fragment classes created successfully!")
    print("="*70)

    print("\nCreated Utility Classes:")
    print("✓ DateUtil.java - Date formatting and relative time calculations")
    print("✓ FileUtil.java - File upload, validation, and management")
    print("✓ ImageUtil.java - Image processing, thumbnails, and resizing")

    print("\nCreated WebSocket Classes:")
    print("✓ ChatWebSocketHandler.java - Real-time chat messaging handler")

    print("\nCreated Thymeleaf Fragments:")
    print("✓ sidebar.html - Chat sidebar with search and bulk actions")
    print("✓ message-bubble.html - Message display with different types")
    print("✓ search-bar.html - Advanced search with suggestions")
    print("✓ filter-panel.html - Comprehensive filtering options")

    print("\nUtility Features:")
    print("• Smart date formatting for chat messages[1]")
    print("• File upload with size and type validation[1]")
    print("• Image thumbnail generation and resizing[1]")
    print("• Relative time calculations (e.g., '2 hours ago')[1]")

    print("\nWebSocket Features:")
    print("• Real-time message sending and receiving[1]")
    print("• Typing indicators for live chat experience[1]")
    print("• User join/leave notifications[1]")
    print("• Session management for multiple users[1]")
    print("• Ping/pong for connection health[1]")
    print("• Broadcasting to chat participants[1]")

    print("\nThymeleaf Fragment Features:")
    print("• Reusable chat sidebar component[1]")
    print("• Message bubbles for different message types[1]")
    print("• Advanced search bar with autocomplete[1]")
    print("• Comprehensive filter panel with presets[1]")
    print("• Bulk action support for chats[1]")
    print("• Pin/unpin functionality[1]")
    print("• Image hide/show toggle[1]")
    print("• User status indicators[1]")

    print("\nNext steps:")
    print("1. Update your main application to use WebSocket configuration")
    print("2. Test WebSocket connections")
    print("3. Test file upload functionality")
    print("4. Integrate fragments into your main dashboard template")
    print("5. Test real-time messaging")
    print("6. Test image processing utilities")

if __name__ == "__main__":
    create_util_websocket_and_fragments()