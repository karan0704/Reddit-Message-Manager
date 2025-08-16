package com.anuj.redditmessagemanager.dto;

import com.anuj.redditmessagemanager.entity.ExportRequest;

import java.time.LocalDateTime;
import java.util.List;

public class ExportRequestDTO {

    private Long id;
    private String exportId;
    private String username;
    private ExportRequest.ExportFormat exportFormat;
    private ExportRequest.ExportStatus exportStatus;
    private LocalDateTime createdAt;
    private LocalDateTime completedAt;
    private LocalDateTime dateFrom;
    private LocalDateTime dateTo;
    private Boolean includeImages;
    private Boolean includeMetadata;
    private Boolean includeSystemMessages;
    private Integer maxMessages;
    private String filePath;
    private Long fileSize;
    private String downloadUrl;
    private Integer messageCount;
    private Integer progressPercentage;
    private String statusMessage;
    private String errorMessage;
    private List<Long> chatIds;

    // Constructors
    public ExportRequestDTO() {}

    public ExportRequestDTO(ExportRequest exportRequest) {
        this.id = exportRequest.getId();
        this.exportId = exportRequest.getExportId();
        this.username = exportRequest.getUser() != null ? exportRequest.getUser().getUsername() : null;
        this.exportFormat = exportRequest.getExportFormat();
        this.exportStatus = exportRequest.getExportStatus();
        this.createdAt = exportRequest.getCreatedAt();
        this.completedAt = exportRequest.getCompletedAt();
        this.dateFrom = exportRequest.getDateFrom();
        this.dateTo = exportRequest.getDateTo();
        this.includeImages = exportRequest.getIncludeImages();
        this.includeMetadata = exportRequest.getIncludeMetadata();
        this.includeSystemMessages = exportRequest.getIncludeSystemMessages();
        this.maxMessages = exportRequest.getMaxMessages();
        this.filePath = exportRequest.getFilePath();
        this.fileSize = exportRequest.getFileSize();
        this.downloadUrl = exportRequest.getDownloadUrl();
        this.messageCount = exportRequest.getMessageCount();
        this.progressPercentage = exportRequest.getProgressPercentage();
        this.statusMessage = exportRequest.getStatusMessage();
        this.errorMessage = exportRequest.getErrorMessage();
        this.chatIds = exportRequest.getChatIds();
    }

    // Getters and Setters
    public Long getId() {
        return id;
    }

    public void setId(Long id) {
        this.id = id;
    }

    public String getExportId() {
        return exportId;
    }

    public void setExportId(String exportId) {
        this.exportId = exportId;
    }

    public String getUsername() {
        return username;
    }

    public void setUsername(String username) {
        this.username = username;
    }

    public ExportRequest.ExportFormat getExportFormat() {
        return exportFormat;
    }

    public void setExportFormat(ExportRequest.ExportFormat exportFormat) {
        this.exportFormat = exportFormat;
    }

    public ExportRequest.ExportStatus getExportStatus() {
        return exportStatus;
    }

    public void setExportStatus(ExportRequest.ExportStatus exportStatus) {
        this.exportStatus = exportStatus;
    }

    public LocalDateTime getCreatedAt() {
        return createdAt;
    }

    public void setCreatedAt(LocalDateTime createdAt) {
        this.createdAt = createdAt;
    }

    public LocalDateTime getCompletedAt() {
        return completedAt;
    }

    public void setCompletedAt(LocalDateTime completedAt) {
        this.completedAt = completedAt;
    }

    public LocalDateTime getDateFrom() {
        return dateFrom;
    }

    public void setDateFrom(LocalDateTime dateFrom) {
        this.dateFrom = dateFrom;
    }

    public LocalDateTime getDateTo() {
        return dateTo;
    }

    public void setDateTo(LocalDateTime dateTo) {
        this.dateTo = dateTo;
    }

    public Boolean getIncludeImages() {
        return includeImages;
    }

    public void setIncludeImages(Boolean includeImages) {
        this.includeImages = includeImages;
    }

    public Boolean getIncludeMetadata() {
        return includeMetadata;
    }

    public void setIncludeMetadata(Boolean includeMetadata) {
        this.includeMetadata = includeMetadata;
    }

    public Boolean getIncludeSystemMessages() {
        return includeSystemMessages;
    }

    public void setIncludeSystemMessages(Boolean includeSystemMessages) {
        this.includeSystemMessages = includeSystemMessages;
    }

    public Integer getMaxMessages() {
        return maxMessages;
    }

    public void setMaxMessages(Integer maxMessages) {
        this.maxMessages = maxMessages;
    }

    public String getFilePath() {
        return filePath;
    }

    public void setFilePath(String filePath) {
        this.filePath = filePath;
    }

    public Long getFileSize() {
        return fileSize;
    }

    public void setFileSize(Long fileSize) {
        this.fileSize = fileSize;
    }

    public String getDownloadUrl() {
        return downloadUrl;
    }

    public void setDownloadUrl(String downloadUrl) {
        this.downloadUrl = downloadUrl;
    }

    public Integer getMessageCount() {
        return messageCount;
    }

    public void setMessageCount(Integer messageCount) {
        this.messageCount = messageCount;
    }

    public Integer getProgressPercentage() {
        return progressPercentage;
    }

    public void setProgressPercentage(Integer progressPercentage) {
        this.progressPercentage = progressPercentage;
    }

    public String getStatusMessage() {
        return statusMessage;
    }

    public void setStatusMessage(String statusMessage) {
        this.statusMessage = statusMessage;
    }

    public String getErrorMessage() {
        return errorMessage;
    }

    public void setErrorMessage(String errorMessage) {
        this.errorMessage = errorMessage;
    }

    public List<Long> getChatIds() {
        return chatIds;
    }

    public void setChatIds(List<Long> chatIds) {
        this.chatIds = chatIds;
    }
}
