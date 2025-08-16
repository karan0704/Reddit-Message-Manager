package com.anuj.redditmessagemanager.dto;

public class UploadResponseDTO {
    
    private String imageUrl;
    private String fileName;
    private Long fileSize;
    private String contentType;
    private String thumbnailUrl;

    // Constructors
    public UploadResponseDTO() {}

    public UploadResponseDTO(String imageUrl, String fileName, Long fileSize, String contentType) {
        this.imageUrl = imageUrl;
        this.fileName = fileName;
        this.fileSize = fileSize;
        this.contentType = contentType;
    }

    // Getters and Setters
    public String getImageUrl() {
        return imageUrl;
    }

    public void setImageUrl(String imageUrl) {
        this.imageUrl = imageUrl;
    }

    public String getFileName() {
        return fileName;
    }

    public void setFileName(String fileName) {
        this.fileName = fileName;
    }

    public Long getFileSize() {
        return fileSize;
    }

    public void setFileSize(Long fileSize) {
        this.fileSize = fileSize;
    }

    public String getContentType() {
        return contentType;
    }

    public void setContentType(String contentType) {
        this.contentType = contentType;
    }

    public String getThumbnailUrl() {
        return thumbnailUrl;
    }

    public void setThumbnailUrl(String thumbnailUrl) {
        this.thumbnailUrl = thumbnailUrl;
    }
}
