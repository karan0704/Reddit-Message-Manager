package com.anuj.redditmessagemanager.service;

import com.anuj.redditmessagemanager.dto.MessageDto;
import com.anuj.redditmessagemanager.entity.Chat;
import com.anuj.redditmessagemanager.entity.Message;
import com.anuj.redditmessagemanager.entity.Message.MessageType;
import com.anuj.redditmessagemanager.entity.UnreadMessage;
import com.anuj.redditmessagemanager.repository.ChatRepository;
import com.anuj.redditmessagemanager.repository.MessageRepository;
import com.anuj.redditmessagemanager.repository.UnreadMessageRepository;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.domain.PageRequest;
import org.springframework.data.domain.Pageable;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.util.List;
import java.util.stream.Collectors;

@Service
@Transactional
public class MessageService {
    
    private static final Logger logger = LoggerFactory.getLogger(MessageService.class);
    
    @Autowired
    private MessageRepository messageRepository;
    
    @Autowired
    private ChatRepository chatRepository;
    
    @Autowired
    private UnreadMessageRepository unreadMessageRepository;
    
    /**
     * Get messages for a chat with pagination
     */
    public List<MessageDto> getChatMessages(Long chatId, String username, int page, int size) {
        try {
            Pageable pageable = PageRequest.of(page, size);
            List<Message> messages = messageRepository.findLatestMessagesByChatId(chatId, pageable);
            
            return messages.stream()
                    .map(message -> convertToDto(message, username))
                    .collect(Collectors.toList());
                    
        } catch (Exception e) {
            logger.error("Error getting chat messages: {}", e.getMessage());
            return List.of();
        }
    }
    
    /**
     * Send message in chat
     */
    public MessageDto sendMessage(Long chatId, String senderUsername, MessageDto messageDto) {
        try {
            Chat chat = chatRepository.findById(chatId).orElse(null);
            if (chat == null) {
                throw new RuntimeException("Chat not found");
            }
            
            // Create message
            Message message = new Message();
            message.setChat(chat);
            message.setSenderUsername(senderUsername);
            message.setMessageContent(messageDto.getMessageContent());
            message.setMessageType(messageDto.getMessageType() != null 
                ? messageDto.getMessageType() : MessageType.TEXT);
            message.setImageUrl(messageDto.getImageUrl());
            message.setIsRead(false);
            message.setIsDeleted(false);
            message.setIsImageHidden(message.getMessageType() == MessageType.IMAGE);
            
            Message savedMessage = messageRepository.save(message);
            
            // Update chat with last message info
            String lastMessagePreview = messageDto.getMessageContent();
            if (lastMessagePreview != null && lastMessagePreview.length() > 50) {
                lastMessagePreview = lastMessagePreview.substring(0, 50) + "...";
            }
            
            chatRepository.updateChatLastMessage(
                chatId, 
                lastMessagePreview, 
                LocalDateTime.now(), 
                true, 
                1
            );
            
            // Create unread message entry for the other user
            String otherUsername = getOtherUsername(chat, senderUsername);
            if (otherUsername != null) {
                UnreadMessage unreadMessage = new UnreadMessage(savedMessage, otherUsername);
                unreadMessageRepository.save(unreadMessage);
            }
            
            logger.info("Message sent from {} in chat {}", senderUsername, chatId);
            
            return convertToDto(savedMessage, senderUsername);
            
        } catch (Exception e) {
            logger.error("Error sending message: {}", e.getMessage());
            throw new RuntimeException("Failed to send message", e);
        }
    }
    
    /**
     * Search messages by content
     */
    public List<MessageDto> searchMessages(String username, String searchTerm, Long chatId) {
        try {
            List<Message> messages;
            
            if (chatId != null) {
                messages = messageRepository.searchMessagesByContent(chatId, searchTerm);
            } else {
                messages = messageRepository.searchAllMessagesByContent(username, searchTerm);
            }
            
            return messages.stream()
                    .map(message -> convertToDto(message, username))
                    .collect(Collectors.toList());
                    
        } catch (Exception e) {
            logger.error("Error searching messages: {}", e.getMessage());
            return List.of();
        }
    }
    
    /**
     * Toggle image visibility in chat
     */
    public boolean toggleImageVisibility(Long chatId, String username) {
        try {
            Chat chat = chatRepository.findById(chatId).orElse(null);
            if (chat == null || !isUserInChat(chat, username)) {
                throw new RuntimeException("Chat not found or access denied");
            }
            
            // Get current visibility status
            List<Message> imageMessages = messageRepository.findImageMessagesByHiddenStatus(chatId, true);
            boolean currentlyHidden = !imageMessages.isEmpty();
            
            // Toggle visibility
            boolean newVisibility = currentlyHidden;
            messageRepository.toggleImageVisibilityInChat(chatId, !newVisibility);
            
            logger.info("Image visibility toggled in chat {} by user {}: {}", 
                chatId, username, newVisibility ? "visible" : "hidden");
            
            return newVisibility;
            
        } catch (Exception e) {
            logger.error("Error toggling image visibility: {}", e.getMessage());
            throw new RuntimeException("Failed to toggle image visibility", e);
        }
    }
    
    /**
     * Mark messages as read in chat
     */
    public void markMessagesAsRead(Long chatId, String username) {
        try {
            messageRepository.markMessagesAsRead(chatId, username);
            unreadMessageRepository.markMessagesAsReadInChat(chatId, username, LocalDateTime.now());
            
            logger.info("Messages marked as read in chat {} by user {}", chatId, username);
            
        } catch (Exception e) {
            logger.error("Error marking messages as read: {}", e.getMessage());
        }
    }
    
    /**
     * Get unread messages for user
     */
    public List<MessageDto> getUnreadMessages(String username) {
        try {
            List<UnreadMessage> unreadMessages = unreadMessageRepository
                .findByUserUsernameAndReadAtIsNullOrderByCreatedAtDesc(username);
            
            return unreadMessages.stream()
                    .map(unread -> convertToDto(unread.getMessage(), username))
                    .collect(Collectors.toList());
                    
        } catch (Exception e) {
            logger.error("Error getting unread messages: {}", e.getMessage());
            return List.of();
        }
    }
    
    /**
     * Delete messages (soft delete)
     */
    public void deleteMessages(List<Long> messageIds, String username) {
        try {
            // Verify user has permission to delete these messages
            for (Long messageId : messageIds) {
                Message message = messageRepository.findById(messageId).orElse(null);
                if (message == null || !canUserDeleteMessage(message, username)) {
                    throw new RuntimeException("Cannot delete message " + messageId);
                }
            }
            
            messageRepository.softDeleteMessages(messageIds);
            logger.info("User {} deleted {} messages", username, messageIds.size());
            
        } catch (Exception e) {
            logger.error("Error deleting messages: {}", e.getMessage());
            throw new RuntimeException("Failed to delete messages", e);
        }
    }
    
    /**
     * Get messages for export
     */
    public List<MessageDto> getMessagesForExport(List<Long> chatIds, String username, 
                                                LocalDateTime startDate, LocalDateTime endDate) {
        try {
            List<Message> messages = messageRepository.findMessagesForExport(chatIds, startDate, endDate);
            
            // Filter messages to only include chats the user participates in
            return messages.stream()
                    .filter(message -> isUserInChat(message.getChat(), username))
                    .map(message -> convertToDto(message, username))
                    .collect(Collectors.toList());
                    
        } catch (Exception e) {
            logger.error("Error getting messages for export: {}", e.getMessage());
            return List.of();
        }
    }
    
    /**
     * Convert Message entity to DTO
     */
    private MessageDto convertToDto(Message message, String currentUsername) {
        MessageDto dto = new MessageDto();
        dto.setId(message.getId());
        dto.setChatId(message.getChat().getId());
        dto.setSenderUsername(message.getSenderUsername());
        dto.setMessageContent(message.getMessageContent());
        dto.setMessageType(message.getMessageType());
        dto.setImageUrl(message.getImageUrl());
        dto.setIsRead(message.getIsRead());
        dto.setIsDeleted(message.getIsDeleted());
        dto.setIsImageHidden(message.getIsImageHidden());
        dto.setCreatedAt(message.getCreatedAt());
        
        // Helper fields
        dto.setIsOwnMessage(message.getSenderUsername().equals(currentUsername));
        dto.setFormattedTime(formatMessageTime(message.getCreatedAt()));
        
        return dto;
    }
    
    /**
     * Format message timestamp for display
     */
    private String formatMessageTime(LocalDateTime timestamp) {
        if (timestamp == null) {
            return "";
        }
        
        LocalDateTime now = LocalDateTime.now();
        if (timestamp.toLocalDate().equals(now.toLocalDate())) {
            // Same day, show time only
            return timestamp.format(DateTimeFormatter.ofPattern("HH:mm"));
        } else {
            // Different day, show date and time
            return timestamp.format(DateTimeFormatter.ofPattern("MMM dd, HH:mm"));
        }
    }
    
    /**
     * Get the other user's username from a chat
     */
    private String getOtherUsername(Chat chat, String currentUsername) {
        return chat.getUser1Username().equals(currentUsername) 
            ? chat.getUser2Username() 
            : chat.getUser1Username();
    }
    
    /**
     * Check if user is part of the chat
     */
    private boolean isUserInChat(Chat chat, String username) {
        return chat.getUser1Username().equals(username) || chat.getUser2Username().equals(username);
    }
    
    /**
     * Check if user can delete a message
     */
    private boolean canUserDeleteMessage(Message message, String username) {
        // User can delete their own messages or any message in chats they participate in
        return message.getSenderUsername().equals(username) || 
               isUserInChat(message.getChat(), username);
    }
}
