package com.anuj.redditmessagemanager.util;

import com.anuj.redditmessagemanager.dto.RedditApiMessageResponse;
import com.anuj.redditmessagemanager.dto.RedditMessageDto;
import com.anuj.redditmessagemanager.entity.RedditMessage;
import com.anuj.redditmessagemanager.entity.RedditMessage.MessageType;
import com.anuj.redditmessagemanager.entity.User;
import org.springframework.stereotype.Component;

import java.time.LocalDateTime;
import java.time.ZoneOffset;
import java.util.ArrayList;
import java.util.Base64;
import java.util.List;
import java.util.UUID;

@Component
public class RedditApiUtil {

    /**
     * Create Basic Auth header for Reddit API
     */
    public String createBasicAuthHeader(String clientId, String clientSecret) {
        String credentials = clientId + ":" + clientSecret;
        return "Basic " + Base64.getEncoder().encodeToString(credentials.getBytes());
    }

    /**
     * Generate random state for OAuth
     */
    public String generateState() {
        return UUID.randomUUID().toString();
    }

    /**
     * Convert Reddit API response to message entities
     */
    public List<RedditMessage> convertApiResponseToMessages(RedditApiMessageResponse response, User user, MessageType messageType) {
        List<RedditMessage> messages = new ArrayList<>();

        if (response.getData() != null && response.getData().getChildren() != null) {
            for (RedditApiMessageResponse.MessageChild child : response.getData().getChildren()) {
                RedditApiMessageResponse.MessageDetails details = child.getData();

                RedditMessage message = new RedditMessage();
                message.setRedditMessageId(details.getId());
                message.setMessageType(messageType);
                message.setSubject(details.getSubject());
                message.setBody(details.getBody() != null ? details.getBody() : details.getBodyHtml());
                message.setAuthor(details.getAuthor());
                message.setRecipient(details.getDest());
                message.setSubreddit(details.getSubreddit());
                message.setIsRead(details.getIsNew() == null || !details.getIsNew());
                message.setContext(details.getContext());
                message.setParentId(details.getParentId());
                message.setUser(user);

                // Convert Reddit timestamp
                if (details.getCreatedUtc() != null) {
                    message.setRedditCreatedAt(
                            LocalDateTime.ofEpochSecond(details.getCreatedUtc().longValue(), 0, ZoneOffset.UTC)
                    );
                }

                messages.add(message);
            }
        }

        return messages;
    }

    /**
     * Convert message entity to DTO
     */
    public RedditMessageDto convertToDto(RedditMessage message) {
        RedditMessageDto dto = new RedditMessageDto();
        dto.setId(message.getId());
        dto.setRedditMessageId(message.getRedditMessageId());
        dto.setMessageType(message.getMessageType());
        dto.setSubject(message.getSubject());
        dto.setBody(message.getBody());
        dto.setAuthor(message.getAuthor());
        dto.setRecipient(message.getRecipient());
        dto.setSubreddit(message.getSubreddit());
        dto.setIsRead(message.getIsRead());
        dto.setRedditCreatedAt(message.getRedditCreatedAt());
        dto.setContext(message.getContext());
        dto.setParentId(message.getParentId());
        dto.setStoredAt(message.getStoredAt());

        return dto;
    }

    /**
     * Convert list of messages to DTOs
     */
    public List<RedditMessageDto> convertToDtoList(List<RedditMessage> messages) {
        List<RedditMessageDto> dtos = new ArrayList<>();
        for (RedditMessage message : messages) {
            dtos.add(convertToDto(message));
        }
        return dtos;
    }

    /**
     * Calculate token expiry time
     */
    public LocalDateTime calculateTokenExpiry(Integer expiresInSeconds) {
        return LocalDateTime.now().plusSeconds(expiresInSeconds);
    }

    /**
     * Check if token is expired
     */
    public boolean isTokenExpired(LocalDateTime expiryTime) {
        return expiryTime != null && expiryTime.isBefore(LocalDateTime.now());
    }

    /**
     * Clean HTML from message body
     */
    /**
     * Clean HTML from message body
     */
    public String cleanHtmlFromBody(String htmlBody) {
        if (htmlBody == null) {
            return null;
        }

        return htmlBody
                .replaceAll("<[^>]+>", "") // Remove HTML tags
                .replaceAll("&amp;", "&")  // Replace HTML entities
                .replaceAll("&lt;", "<")
                .replaceAll("&gt;", ">")
                .replaceAll("&quot;", "\"")
                .replaceAll("&apos;", "'")
                .replaceAll("&#x27;", "'")
                .replaceAll("&#x2F;", "/")
                .trim();
    }
}