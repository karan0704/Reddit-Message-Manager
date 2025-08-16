package com.anuj.redditmessagemanager.service;

import com.anuj.redditmessagemanager.dto.ChatDto;
import com.anuj.redditmessagemanager.dto.BulkActionDto;
import com.anuj.redditmessagemanager.entity.Chat;
import com.anuj.redditmessagemanager.entity.PinnedChat;
import com.anuj.redditmessagemanager.repository.ChatRepository;
import com.anuj.redditmessagemanager.repository.PinnedChatRepository;
import com.anuj.redditmessagemanager.repository.BlockedUserRepository;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.time.LocalDateTime;
import java.util.List;
import java.util.Map;
import java.util.HashMap;
import java.util.stream.Collectors;

@Service
@Transactional
public class ChatService {
    
    private static final Logger logger = LoggerFactory.getLogger(ChatService.class);
    
    @Autowired
    private ChatRepository chatRepository;
    
    @Autowired
    private PinnedChatRepository pinnedChatRepository;
    
    @Autowired
    private BlockedUserRepository blockedUserRepository;
    
    /**
     * Get all chats for a user
     */
    public List<ChatDto> getUserChats(String username) {
        try {
            List<Chat> chats = chatRepository.findChatsByUsernameOrderByActivity(username);
            
            return chats.stream()
                    .filter(chat -> !isUserBlocked(username, getOtherUsername(chat, username)))
                    .map(chat -> convertToDto(chat, username))
                    .collect(Collectors.toList());
                    
        } catch (Exception e) {
            logger.error("Error getting user chats: {}", e.getMessage());
            return List.of();
        }
    }
    
    /**
     * Get pinned chats for a user
     */
    public List<ChatDto> getPinnedChats(String username) {
        try {
            List<Chat> pinnedChats = chatRepository.findPinnedChatsByUsername(username);
            
            return pinnedChats.stream()
                    .map(chat -> convertToDto(chat, username))
                    .collect(Collectors.toList());
                    
        } catch (Exception e) {
            logger.error("Error getting pinned chats: {}", e.getMessage());
            return List.of();
        }
    }
    
    /**
     * Get chats with unread messages
     */
    public List<ChatDto> getChatsWithUnreadMessages(String username) {
        try {
            List<Chat> unreadChats = chatRepository.findChatsWithUnreadMessages(username);
            
            return unreadChats.stream()
                    .filter(chat -> !isUserBlocked(username, getOtherUsername(chat, username)))
                    .map(chat -> convertToDto(chat, username))
                    .collect(Collectors.toList());
                    
        } catch (Exception e) {
            logger.error("Error getting chats with unread messages: {}", e.getMessage());
            return List.of();
        }
    }
    
    /**
     * Get or create chat between two users
     */
    public ChatDto getOrCreateChat(String user1, String user2) {
        try {
            // Check if users are blocking each other
            if (isUserBlocked(user1, user2) || isUserBlocked(user2, user1)) {
                throw new RuntimeException("Cannot create chat with blocked user");
            }
            
            Chat chat = chatRepository.findChatBetweenUsers(user1, user2).orElse(null);
            
            if (chat == null) {
                chat = new Chat();
                chat.setUser1Username(user1);
                chat.setUser2Username(user2);
                chat.setLastMessageTimestamp(LocalDateTime.now());
                
                chat = chatRepository.save(chat);
                logger.info("Created new chat between {} and {}", user1, user2);
            }
            
            return convertToDto(chat, user1);
            
        } catch (Exception e) {
            logger.error("Error getting or creating chat: {}", e.getMessage());
            throw new RuntimeException("Failed to create chat", e);
        }
    }
    
    /**
     * Mark chat as read
     */
    public void markChatAsRead(Long chatId, String username) {
        try {
            chatRepository.markChatAsRead(chatId);
            logger.info("Chat {} marked as read by user {}", chatId, username);
            
        } catch (Exception e) {
            logger.error("Error marking chat as read: {}", e.getMessage());
        }
    }
    
    /**
     * Toggle pin status of chat
     */
    public boolean togglePinChat(Long chatId, String username) {
        try {
            Chat chat = chatRepository.findById(chatId).orElse(null);
            if (chat == null) {
                throw new RuntimeException("Chat not found");
            }
            
            boolean currentlyPinned = pinnedChatRepository.isChatPinned(chatId, username);
            
            if (currentlyPinned) {
                // Unpin chat
                pinnedChatRepository.unpinChat(chatId, username, LocalDateTime.now());
                logger.info("Chat {} unpinned by user {}", chatId, username);
                return false;
            } else {
                // Pin chat
                Integer nextOrder = pinnedChatRepository.getNextPinOrder(username);
                PinnedChat pinnedChat = new PinnedChat(chat, username, nextOrder);
                pinnedChatRepository.save(pinnedChat);
                logger.info("Chat {} pinned by user {}", chatId, username);
                return true;
            }
            
        } catch (Exception e) {
            logger.error("Error toggling pin status: {}", e.getMessage());
            throw new RuntimeException("Failed to toggle pin status", e);
        }
    }
    
    /**
     * Toggle archive status of chat
     */
    public boolean toggleArchiveChat(Long chatId, String username) {
        try {
            Chat chat = chatRepository.findById(chatId).orElse(null);
            if (chat == null) {
                throw new RuntimeException("Chat not found");
            }
            
            boolean newArchiveStatus = !chat.getIsArchived();
            chatRepository.updateChatArchiveStatus(chatId, newArchiveStatus);
            
            logger.info("Chat {} {} by user {}", chatId, 
                newArchiveStatus ? "archived" : "unarchived", username);
            
            return newArchiveStatus;
            
        } catch (Exception e) {
            logger.error("Error toggling archive status: {}", e.getMessage());
            throw new RuntimeException("Failed to toggle archive status", e);
        }
    }
    
    /**
     * Process bulk actions on chats
     */
    public int processBulkAction(BulkActionDto bulkAction, String username) {
        try {
            List<Long> chatIds = bulkAction.getChatIds();
            int processedCount = 0;
            
            switch (bulkAction.getActionType()) {
                case DELETE_CHATS:
                    for (Long chatId : chatIds) {
                        Chat chat = chatRepository.findById(chatId).orElse(null);
                        if (chat != null && isUserInChat(chat, username)) {
                            chatRepository.delete(chat);
                            processedCount++;
                        }
                    }
                    logger.info("Bulk deleted {} chats for user {}", processedCount, username);
                    break;
                    
                case PIN_CHATS:
                    for (Long chatId : chatIds) {
                        if (!pinnedChatRepository.isChatPinned(chatId, username)) {
                            Chat chat = chatRepository.findById(chatId).orElse(null);
                            if (chat != null && isUserInChat(chat, username)) {
                                Integer nextOrder = pinnedChatRepository.getNextPinOrder(username);
                                PinnedChat pinnedChat = new PinnedChat(chat, username, nextOrder);
                                pinnedChatRepository.save(pinnedChat);
                                processedCount++;
                            }
                        }
                    }
                    logger.info("Bulk pinned {} chats for user {}", processedCount, username);
                    break;
                    
                case UNPIN_CHATS:
                    pinnedChatRepository.bulkUnpinChats(chatIds, username, LocalDateTime.now());
                    processedCount = chatIds.size();
                    logger.info("Bulk unpinned {} chats for user {}", processedCount, username);
                    break;
                    
                case ARCHIVE_CHATS:
                    for (Long chatId : chatIds) {
                        Chat chat = chatRepository.findById(chatId).orElse(null);
                        if (chat != null && isUserInChat(chat, username)) {
                            chatRepository.updateChatArchiveStatus(chatId, true);
                            processedCount++;
                        }
                    }
                    logger.info("Bulk archived {} chats for user {}", processedCount, username);
                    break;
            }
            
            return processedCount;
            
        } catch (Exception e) {
            logger.error("Error processing bulk action: {}", e.getMessage());
            throw new RuntimeException("Failed to process bulk action", e);
        }
    }
    
    /**
     * Get chat statistics for user
     */
    public Map<String, Object> getChatStatistics(String username) {
        try {
            Map<String, Object> stats = new HashMap<>();
            
            stats.put("totalChats", chatRepository.countChatsByUsername(username));
            stats.put("unreadMessages", chatRepository.countTotalUnreadMessages(username));
            stats.put("pinnedChats", pinnedChatRepository.countPinnedChatsByUser(username));
            stats.put("archivedChats", chatRepository.findArchivedChatsByUsername(username).size());
            
            return stats;
            
        } catch (Exception e) {
            logger.error("Error getting chat statistics: {}", e.getMessage());
            return new HashMap<>();
        }
    }
    
    /**
     * Convert Chat entity to DTO
     */
    private ChatDto convertToDto(Chat chat, String currentUsername) {
        ChatDto dto = new ChatDto();
        dto.setId(chat.getId());
        dto.setUser1Username(chat.getUser1Username());
        dto.setUser2Username(chat.getUser2Username());
        dto.setOtherUsername(getOtherUsername(chat, currentUsername));
        dto.setLastMessage(chat.getLastMessage());
        dto.setLastMessageTimestamp(chat.getLastMessageTimestamp());
        dto.setIsPinned(chat.getIsPinned());
        dto.setHasUnread(chat.getHasUnread());
        dto.setUnreadCount(chat.getUnreadCount());
        dto.setCreatedAt(chat.getCreatedAt());
        dto.setUpdatedAt(chat.getUpdatedAt());
        
        return dto;
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
     * Check if user is blocked
     */
    private boolean isUserBlocked(String blocker, String blocked) {
        return blockedUserRepository.isUserBlocked(blocker, blocked);
    }
}
