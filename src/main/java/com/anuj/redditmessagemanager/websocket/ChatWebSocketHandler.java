package com.anuj.redditmessagemanager.websocket;

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
