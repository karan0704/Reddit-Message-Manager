package com.anuj.redditmessagemanager.dto;

import com.fasterxml.jackson.annotation.JsonProperty;
import lombok.Data;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;

import java.time.LocalDateTime;
import java.util.List;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class ExportDto {
    
    @JsonProperty("export_format")
    private ExportFormat exportFormat;
    
    @JsonProperty("chat_ids")
    private List<Long> chatIds;
    
    @JsonProperty("date_from")
    private LocalDateTime dateFrom;
    
    @JsonProperty("date_to")
    private LocalDateTime dateTo;
    
    @JsonProperty("include_images")
    private Boolean includeImages;
    
    @JsonProperty("include_metadata")
    private Boolean includeMetadata;
    
    @JsonProperty("max_messages")
    private Integer maxMessages;
    
    @JsonProperty("filename")
    private String filename;
    
    @JsonProperty("export_size_mb")
    private Double exportSizeMb;
    
    @JsonProperty("message_count")
    private Integer messageCount;
    
    @JsonProperty("download_url")
    private String downloadUrl;
    
    @JsonProperty("export_status")
    private ExportStatus exportStatus;
    
    @JsonProperty("created_at")
    private LocalDateTime createdAt;
    
    @JsonProperty("completed_at")
    private LocalDateTime completedAt;
    
    @JsonProperty("error_message")
    private String errorMessage;
    
    public enum ExportFormat {
        TXT, JSON, CSV, HTML, PDF
    }
    
    public enum ExportStatus {
        PENDING, IN_PROGRESS, COMPLETED, FAILED, EXPIRED
    }
    
    // Constructor for export request
    public ExportDto(ExportFormat exportFormat, List<Long> chatIds, LocalDateTime dateFrom, 
                    LocalDateTime dateTo, Boolean includeImages) {
        this.exportFormat = exportFormat;
        this.chatIds = chatIds;
        this.dateFrom = dateFrom;
        this.dateTo = dateTo;
        this.includeImages = includeImages != null ? includeImages : false;
        this.includeMetadata = true;
        this.maxMessages = 10000;
        this.exportStatus = ExportStatus.PENDING;
        this.createdAt = LocalDateTime.now();
    }
    
    // Constructor for export response
    public ExportDto(String filename, Double exportSizeMb, Integer messageCount, 
                    String downloadUrl, ExportStatus status) {
        this.filename = filename;
        this.exportSizeMb = exportSizeMb;
        this.messageCount = messageCount;
        this.downloadUrl = downloadUrl;
        this.exportStatus = status;
    }
}
