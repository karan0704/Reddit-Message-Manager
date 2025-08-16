package com.anuj.redditmessagemanager.util;

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
