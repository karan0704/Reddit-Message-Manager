package com.anuj.redditmessagemanager.util;

import org.springframework.stereotype.Component;

import java.time.LocalDateTime;
import java.time.ZoneOffset;
import java.time.format.DateTimeFormatter;
import java.time.temporal.ChronoUnit;

@Component
public class DateTimeUtil {
    
    private static final DateTimeFormatter DISPLAY_FORMATTER = DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss");
    private static final DateTimeFormatter FILE_SAFE_FORMATTER = DateTimeFormatter.ofPattern("yyyy-MM-dd_HH-mm-ss");
    
    /**
     * Convert Unix timestamp to LocalDateTime
     */
    public LocalDateTime fromUnixTimestamp(Long timestamp) {
        if (timestamp == null) {
            return null;
        }
        return LocalDateTime.ofEpochSecond(timestamp, 0, ZoneOffset.UTC);
    }
    
    /**
     * Convert Unix timestamp (Double) to LocalDateTime
     */
    public LocalDateTime fromUnixTimestamp(Double timestamp) {
        if (timestamp == null) {
            return null;
        }
        return LocalDateTime.ofEpochSecond(timestamp.longValue(), 0, ZoneOffset.UTC);
    }
    
    /**
     * Convert LocalDateTime to Unix timestamp
     */
    public Long toUnixTimestamp(LocalDateTime dateTime) {
        if (dateTime == null) {
            return null;
        }
        return dateTime.toEpochSecond(ZoneOffset.UTC);
    }
    
    /**
     * Format DateTime for display
     */
    public String formatForDisplay(LocalDateTime dateTime) {
        if (dateTime == null) {
            return "N/A";
        }
        return dateTime.format(DISPLAY_FORMATTER);
    }
    
    /**
     * Format DateTime for filename
     */
    public String formatForFilename(LocalDateTime dateTime) {
        if (dateTime == null) {
            return "unknown";
        }
        return dateTime.format(FILE_SAFE_FORMATTER);
    }
    
    /**
     * Get relative time string
     */
    public String getRelativeTime(LocalDateTime dateTime) {
        if (dateTime == null) {
            return "Unknown time";
        }
        
        LocalDateTime now = LocalDateTime.now();
        long minutes = ChronoUnit.MINUTES.between(dateTime, now);
        long hours = ChronoUnit.HOURS.between(dateTime, now);
        long days = ChronoUnit.DAYS.between(dateTime, now);
        
        if (minutes < 1) {
            return "Just now";
        } else if (minutes < 60) {
            return minutes + " minute" + (minutes == 1 ? "" : "s") + " ago";
        } else if (hours < 24) {
            return hours + " hour" + (hours == 1 ? "" : "s") + " ago";
        } else if (days < 7) {
            return days + " day" + (days == 1 ? "" : "s") + " ago";
        } else {
            return formatForDisplay(dateTime);
        }
    }
    
    /**
     * Check if DateTime is recent (within last hour)
     */
    public boolean isRecent(LocalDateTime dateTime) {
        if (dateTime == null) {
            return false;
        }
        return ChronoUnit.HOURS.between(dateTime, LocalDateTime.now()) <= 1;
    }
    
    /**
     * Check if DateTime is today
     */
    public boolean isToday(LocalDateTime dateTime) {
        if (dateTime == null) {
            return false;
        }
        return dateTime.toLocalDate().equals(LocalDateTime.now().toLocalDate());
    }
    
    /**
     * Get start of day
     */
    public LocalDateTime getStartOfDay(LocalDateTime dateTime) {
        if (dateTime == null) {
            return null;
        }
        return dateTime.truncatedTo(ChronoUnit.DAYS);
    }
    
    /**
     * Get end of day
     */
    public LocalDateTime getEndOfDay(LocalDateTime dateTime) {
        if (dateTime == null) {
            return null;
        }
        return dateTime.truncatedTo(ChronoUnit.DAYS).plusDays(1).minusNanos(1);
    }
}
