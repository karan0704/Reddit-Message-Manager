package com.anuj.redditmessagemanager.service;

import com.anuj.redditmessagemanager.dto.ExportDto;
import com.anuj.redditmessagemanager.dto.MessageDto;
import com.anuj.redditmessagemanager.dto.ExportDto.ExportFormat;
import com.anuj.redditmessagemanager.dto.ExportDto.ExportStatus;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.core.io.Resource;
import org.springframework.core.io.UrlResource;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.io.FileWriter;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.util.List;
import java.util.Map;
import java.util.concurrent.ConcurrentHashMap;

@Service
@Transactional
public class ExportService {
    
    private static final Logger logger = LoggerFactory.getLogger(ExportService.class);
    
    @Autowired
    private MessageService messageService;
    
    @Autowired
    private ObjectMapper objectMapper;
    
    // In-memory storage for export status (in production, use database or cache)
    private final Map<String, ExportDto> exportStatusMap = new ConcurrentHashMap<>();
    
    private static final String EXPORT_DIR = "./exports/";
    
    /**
     * Export chats to file
     */
    public ExportDto exportChats(String username, ExportDto exportRequest) {
        try {
            String exportId = generateExportId(username);
            
            // Create export directory if it doesn't exist
            Files.createDirectories(Paths.get(EXPORT_DIR));
            
            // Initialize export status
            ExportDto exportStatus = new ExportDto();
            exportStatus.setExportFormat(exportRequest.getExportFormat());
            exportStatus.setChatIds(exportRequest.getChatIds());
            exportStatus.setDateFrom(exportRequest.getDateFrom());
            exportStatus.setDateTo(exportRequest.getDateTo());
            exportStatus.setIncludeImages(exportRequest.getIncludeImages());
            exportStatus.setIncludeMetadata(exportRequest.getIncludeMetadata());
            exportStatus.setMaxMessages(exportRequest.getMaxMessages());
            exportStatus.setExportStatus(ExportStatus.PENDING);
            exportStatus.setCreatedAt(LocalDateTime.now());
            
            // Generate filename
            String filename = generateFilename(username, exportRequest.getExportFormat());
            exportStatus.setFilename(filename);
            
            exportStatusMap.put(exportId, exportStatus);
            
            // Start export process asynchronously (simplified version)
            processExport(exportId, username, exportRequest);
            
            logger.info("Export started for user {}: {}", username, exportId);
            
            exportStatus.setDownloadUrl("/api/export/download/" + filename);
            return exportStatus;
            
        } catch (Exception e) {
            logger.error("Error starting export: {}", e.getMessage());
            throw new RuntimeException("Failed to start export: " + e.getMessage(), e);
        }
    }
    
    /**
     * Process export (simplified synchronous version)
     */
    private void processExport(String exportId, String username, ExportDto exportRequest) {
        try {
            ExportDto status = exportStatusMap.get(exportId);
            status.setExportStatus(ExportStatus.IN_PROGRESS);
            
            // Get messages to export
            List<MessageDto> messages = messageService.getMessagesForExport(
                exportRequest.getChatIds(),
                username,
                exportRequest.getDateFrom(),
                exportRequest.getDateTo()
            );
            
            // Apply message limit
            if (exportRequest.getMaxMessages() != null && messages.size() > exportRequest.getMaxMessages()) {
                messages = messages.subList(0, exportRequest.getMaxMessages());
            }
            
            // Export to appropriate format
            Path filePath = Paths.get(EXPORT_DIR + status.getFilename());
            
            switch (exportRequest.getExportFormat()) {
                case TXT:
                    exportToTxt(messages, filePath, exportRequest.getIncludeMetadata());
                    break;
                case JSON:
                    exportToJson(messages, filePath);
                    break;
                case CSV:
                    exportToCsv(messages, filePath);
                    break;
                default:
                    throw new RuntimeException("Unsupported export format");
            }
            
            // Update status
            status.setExportStatus(ExportStatus.COMPLETED);
            status.setCompletedAt(LocalDateTime.now());
            status.setMessageCount(messages.size());
            status.setExportSizeMb(Files.size(filePath) / (1024.0 * 1024.0));
            
            logger.info("Export completed for user {}: {} messages exported", username, messages.size());
            
        } catch (Exception e) {
            logger.error("Error processing export: {}", e.getMessage());
            
            ExportDto status = exportStatusMap.get(exportId);
            if (status != null) {
                status.setExportStatus(ExportStatus.FAILED);
                status.setErrorMessage(e.getMessage());
            }
        }
    }
    
    /**
     * Export messages to TXT format
     */
    private void exportToTxt(List<MessageDto> messages, Path filePath, Boolean includeMetadata) throws IOException {
        try (FileWriter writer = new FileWriter(filePath.toFile())) {
            writer.write("Chat Export - " + LocalDateTime.now().format(DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss")) + "\n");
            writer.write("=" + "=".repeat(50) + "\n\n");
            
            for (MessageDto message : messages) {
                if (includeMetadata) {
                    writer.write("From: " + message.getSenderUsername() + "\n");
                    writer.write("Time: " + (message.getCreatedAt() != null ? 
                        message.getCreatedAt().format(DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss")) : "Unknown") + "\n");
                    writer.write("Chat ID: " + message.getChatId() + "\n");
                    writer.write("Type: " + message.getMessageType() + "\n");
                }
                
                writer.write("Message: " + (message.getMessageContent() != null ? message.getMessageContent() : "[No content]") + "\n");
                
                if (message.getImageUrl() != null) {
                    writer.write("Image: " + message.getImageUrl() + "\n");
                }
                
                writer.write("\n" + "-".repeat(50) + "\n\n");
            }
        }
    }
    
    /**
     * Export messages to JSON format
     */
    private void exportToJson(List<MessageDto> messages, Path filePath) throws IOException {
        Map<String, Object> exportData = Map.of(
            "exportedAt", LocalDateTime.now(),
            "messageCount", messages.size(),
            "messages", messages
        );
        
        objectMapper.writeValue(filePath.toFile(), exportData);
    }
    
    /**
     * Export messages to CSV format
     */
    private void exportToCsv(List<MessageDto> messages, Path filePath) throws IOException {
        try (FileWriter writer = new FileWriter(filePath.toFile())) {
            // CSV header
            writer.write("ID,Chat ID,Sender,Message,Type,Created At,Image URL\n");
            
            // CSV data
            for (MessageDto message : messages) {
                writer.write(String.format("%d,%d,\"%s\",\"%s\",%s,%s,\"%s\"\n",
                    message.getId(),
                    message.getChatId(),
                    escapeForCsv(message.getSenderUsername()),
                    escapeForCsv(message.getMessageContent()),
                    message.getMessageType(),
                    message.getCreatedAt() != null ? message.getCreatedAt().toString() : "",
                    message.getImageUrl() != null ? message.getImageUrl() : ""
                ));
            }
        }
    }
    
    /**
     * Get exported file for download
     */
    public Resource getExportedFile(String username, String filename) throws Exception {
        try {
            Path filePath = Paths.get(EXPORT_DIR + filename);
            
            if (!Files.exists(filePath)) {
                throw new RuntimeException("File not found: " + filename);
            }
            
            Resource resource = new UrlResource(filePath.toUri());
            
            if (resource.exists() && resource.isReadable()) {
                return resource;
            } else {
                throw new RuntimeException("Could not read file: " + filename);
            }
            
        } catch (Exception e) {
            logger.error("Error getting exported file: {}", e.getMessage());
            throw new RuntimeException("Failed to get file: " + e.getMessage(), e);
        }
    }
    
    /**
     * Get export status
     */
    public ExportDto getExportStatus(String username, String exportId) {
        ExportDto status = exportStatusMap.get(exportId);
        
        if (status == null) {
            throw new RuntimeException("Export not found: " + exportId);
        }
        
        return status;
    }
    
    /**
     * Generate unique export ID
     */
    private String generateExportId(String username) {
        return username + "_" + System.currentTimeMillis();
    }
    
    /**
     * Generate filename for export
     */
    private String generateFilename(String username, ExportFormat format) {
        String timestamp = LocalDateTime.now().format(DateTimeFormatter.ofPattern("yyyyMMdd_HHmmss"));
        String extension = format.name().toLowerCase();
        
        return String.format("chat_export_%s_%s.%s", username, timestamp, extension);
    }
    
    /**
     * Escape text for CSV format
     */
    private String escapeForCsv(String text) {
        if (text == null) {
            return "";
        }
        
        return text.replace("\"", "\"\"").replace("\n", " ").replace("\r", " ");
    }
    
    /**
     * Clean up old export files
     */
    public void cleanupOldExports() {
        try {
            Path exportDir = Paths.get(EXPORT_DIR);
            if (!Files.exists(exportDir)) {
                return;
            }
            
            LocalDateTime cutoffTime = LocalDateTime.now().minusDays(7); // Keep files for 7 days
            
            Files.walk(exportDir)
                    .filter(Files::isRegularFile)
                    .filter(path -> {
                        try {
                            return Files.getLastModifiedTime(path)
                                    .toInstant()
                                    .isBefore(cutoffTime.atZone(java.time.ZoneId.systemDefault()).toInstant());
                        } catch (IOException e) {
                            return false;
                        }
                    })
                    .forEach(path -> {
                        try {
                            Files.delete(path);
                            logger.info("Deleted old export file: {}", path.getFileName());
                        } catch (IOException e) {
                            logger.error("Failed to delete old export file: {}", path.getFileName());
                        }
                    });
                    
        } catch (Exception e) {
            logger.error("Error cleaning up old exports: {}", e.getMessage());
        }
    }
}
