import os

def create_missing_java_files():
    # Base path from your project structure
    base_path = "D:\\Karan Ticket Project\\Reddit Message Manager"
    
    # Missing Java files for the Reddit Message Manager
    java_files = [
        {
            "path": "src\\main\\java\\com\\anuj\\redditmessagemanager\\controller\\UploadController.java",
            "content": """package com.anuj.redditmessagemanager.controller;

import com.anuj.redditmessagemanager.dto.UploadResponseDTO;
import com.anuj.redditmessagemanager.service.UploadService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;

import java.util.HashMap;
import java.util.Map;

@RestController
@RequestMapping("/api/upload")
public class UploadController {

    @Autowired
    private UploadService uploadService;

    @PostMapping("/image")
    public ResponseEntity<?> uploadImage(@RequestParam("image") MultipartFile file,
                                       @RequestParam("chatId") Long chatId) {
        try {
            if (file.isEmpty()) {
                return ResponseEntity.badRequest().body(createErrorResponse("No file provided"));
            }

            if (!isImageFile(file)) {
                return ResponseEntity.badRequest().body(createErrorResponse("Only image files are allowed"));
            }

            if (file.getSize() > 10 * 1024 * 1024) { // 10MB limit
                return ResponseEntity.badRequest().body(createErrorResponse("File size too large. Maximum 10MB allowed"));
            }

            String imageUrl = uploadService.uploadImage(file, chatId);
            
            UploadResponseDTO response = new UploadResponseDTO();
            response.setImageUrl(imageUrl);
            response.setFileName(file.getOriginalFilename());
            response.setFileSize(file.getSize());
            response.setContentType(file.getContentType());

            return ResponseEntity.ok(response);

        } catch (Exception e) {
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
                    .body(createErrorResponse("Failed to upload image: " + e.getMessage()));
        }
    }

    @PostMapping("/avatar")
    public ResponseEntity<?> uploadAvatar(@RequestParam("avatar") MultipartFile file) {
        try {
            if (file.isEmpty()) {
                return ResponseEntity.badRequest().body(createErrorResponse("No file provided"));
            }

            if (!isImageFile(file)) {
                return ResponseEntity.badRequest().body(createErrorResponse("Only image files are allowed"));
            }

            if (file.getSize() > 5 * 1024 * 1024) { // 5MB limit for avatars
                return ResponseEntity.badRequest().body(createErrorResponse("File size too large. Maximum 5MB allowed"));
            }

            String avatarUrl = uploadService.uploadAvatar(file);
            
            Map<String, Object> response = new HashMap<>();
            response.put("avatarUrl", avatarUrl);
            response.put("fileName", file.getOriginalFilename());

            return ResponseEntity.ok(response);

        } catch (Exception e) {
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
                    .body(createErrorResponse("Failed to upload avatar: " + e.getMessage()));
        }
    }

    @PostMapping("/file")
    public ResponseEntity<?> uploadFile(@RequestParam("file") MultipartFile file,
                                       @RequestParam("chatId") Long chatId) {
        try {
            if (file.isEmpty()) {
                return ResponseEntity.badRequest().body(createErrorResponse("No file provided"));
            }

            if (file.getSize() > 50 * 1024 * 1024) { // 50MB limit for files
                return ResponseEntity.badRequest().body(createErrorResponse("File size too large. Maximum 50MB allowed"));
            }

            String fileUrl = uploadService.uploadFile(file, chatId);
            
            Map<String, Object> response = new HashMap<>();
            response.put("fileUrl", fileUrl);
            response.put("fileName", file.getOriginalFilename());
            response.put("fileSize", file.getSize());
            response.put("contentType", file.getContentType());

            return ResponseEntity.ok(response);

        } catch (Exception e) {
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
                    .body(createErrorResponse("Failed to upload file: " + e.getMessage()));
        }
    }

    @DeleteMapping("/image/{filename}")
    public ResponseEntity<?> deleteImage(@PathVariable String filename) {
        try {
            boolean deleted = uploadService.deleteFile(filename);
            
            if (deleted) {
                return ResponseEntity.ok().body(Map.of("message", "Image deleted successfully"));
            } else {
                return ResponseEntity.notFound().build();
            }

        } catch (Exception e) {
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
                    .body(createErrorResponse("Failed to delete image: " + e.getMessage()));
        }
    }

    private boolean isImageFile(MultipartFile file) {
        String contentType = file.getContentType();
        return contentType != null && contentType.startsWith("image/");
    }

    private Map<String, String> createErrorResponse(String message) {
        Map<String, String> error = new HashMap<>();
        error.put("error", message);
        return error;
    }
}
"""
        },
        
        {
            "path": "src\\main\\java\\com\\anuj\\redditmessagemanager\\service\\UploadService.java",
            "content": """package com.anuj.redditmessagemanager.service;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;
import org.springframework.web.multipart.MultipartFile;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.nio.file.StandardCopyOption;
import java.util.UUID;

@Service
public class UploadService {

    @Value("${app.upload.dir:uploads}")
    private String uploadDir;

    @Value("${app.upload.images.dir:uploads/images}")
    private String imageUploadDir;

    @Value("${app.upload.avatars.dir:uploads/avatars}")
    private String avatarUploadDir;

    @Value("${app.upload.files.dir:uploads/files}")
    private String fileUploadDir;

    @Value("${app.base.url:http://localhost:8080}")
    private String baseUrl;

    public String uploadImage(MultipartFile file, Long chatId) throws IOException {
        return uploadFile(file, imageUploadDir, "images");
    }

    public String uploadAvatar(MultipartFile file) throws IOException {
        return uploadFile(file, avatarUploadDir, "avatars");
    }

    public String uploadFile(MultipartFile file, Long chatId) throws IOException {
        return uploadFile(file, fileUploadDir, "files");
    }

    private String uploadFile(MultipartFile file, String directory, String urlPath) throws IOException {
        // Create directory if it doesn't exist
        Path uploadPath = Paths.get(directory);
        if (!Files.exists(uploadPath)) {
            Files.createDirectories(uploadPath);
        }

        // Generate unique filename
        String originalFilename = file.getOriginalFilename();
        String extension = "";
        if (originalFilename != null && originalFilename.contains(".")) {
            extension = originalFilename.substring(originalFilename.lastIndexOf("."));
        }
        
        String uniqueFilename = UUID.randomUUID().toString() + extension;
        
        // Save file
        Path filePath = uploadPath.resolve(uniqueFilename);
        Files.copy(file.getInputStream(), filePath, StandardCopyOption.REPLACE_EXISTING);
        
        // Return accessible URL
        return baseUrl + "/" + urlPath + "/" + uniqueFilename;
    }

    public boolean deleteFile(String filename) {
        try {
            // Try to delete from all possible directories
            String[] directories = {imageUploadDir, avatarUploadDir, fileUploadDir};
            
            for (String dir : directories) {
                Path filePath = Paths.get(dir, filename);
                if (Files.exists(filePath)) {
                    Files.delete(filePath);
                    return true;
                }
            }
            
            return false;
        } catch (IOException e) {
            return false;
        }
    }

    public Path getFilePath(String filename, String directory) {
        return Paths.get(directory, filename);
    }

    public boolean fileExists(String filename, String directory) {
        return Files.exists(getFilePath(filename, directory));
    }
}
"""
        },
        
        {
            "path": "src\\main\\java\\com\\anuj\\redditmessagemanager\\entity\\ExportRequest.java",
            "content": """package com.anuj.redditmessagemanager.entity;

import jakarta.persistence.*;
import java.time.LocalDateTime;
import java.util.List;

@Entity
@Table(name = "export_requests")
public class ExportRequest {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false, unique = true)
    private String exportId;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "user_id", nullable = false)
    private User user;

    @Enumerated(EnumType.STRING)
    @Column(nullable = false)
    private ExportFormat exportFormat;

    @Enumerated(EnumType.STRING)
    @Column(nullable = false)
    private ExportStatus exportStatus;

    @Column(name = "created_at", nullable = false)
    private LocalDateTime createdAt;

    @Column(name = "completed_at")
    private LocalDateTime completedAt;

    @Column(name = "date_from")
    private LocalDateTime dateFrom;

    @Column(name = "date_to")
    private LocalDateTime dateTo;

    @Column(name = "include_images")
    private Boolean includeImages = true;

    @Column(name = "include_metadata")
    private Boolean includeMetadata = true;

    @Column(name = "include_system_messages")
    private Boolean includeSystemMessages = false;

    @Column(name = "max_messages")
    private Integer maxMessages;

    @Column(name = "file_path")
    private String filePath;

    @Column(name = "file_size")
    private Long fileSize;

    @Column(name = "download_url")
    private String downloadUrl;

    @Column(name = "message_count")
    private Integer messageCount = 0;

    @Column(name = "progress_percentage")
    private Integer progressPercentage = 0;

    @Column(name = "status_message")
    private String statusMessage;

    @Column(name = "error_message")
    private String errorMessage;

    @ElementCollection
    @CollectionTable(name = "export_chat_ids", joinColumns = @JoinColumn(name = "export_request_id"))
    @Column(name = "chat_id")
    private List<Long> chatIds;

    public enum ExportFormat {
        TXT, JSON, CSV, HTML
    }

    public enum ExportStatus {
        PENDING, IN_PROGRESS, COMPLETED, FAILED, CANCELLED
    }

    // Constructors
    public ExportRequest() {
        this.createdAt = LocalDateTime.now();
        this.exportStatus = ExportStatus.PENDING;
    }

    public ExportRequest(User user, ExportFormat exportFormat) {
        this();
        this.user = user;
        this.exportFormat = exportFormat;
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

    public User getUser() {
        return user;
    }

    public void setUser(User user) {
        this.user = user;
    }

    public ExportFormat getExportFormat() {
        return exportFormat;
    }

    public void setExportFormat(ExportFormat exportFormat) {
        this.exportFormat = exportFormat;
    }

    public ExportStatus getExportStatus() {
        return exportStatus;
    }

    public void setExportStatus(ExportStatus exportStatus) {
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
"""
        },
        
        {
            "path": "src\\main\\java\\com\\anuj\\redditmessagemanager\\repository\\ExportRequestRepository.java",
            "content": """package com.anuj.redditmessagemanager.repository;

import com.anuj.redditmessagemanager.entity.ExportRequest;
import com.anuj.redditmessagemanager.entity.User;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.time.LocalDateTime;
import java.util.List;
import java.util.Optional;

@Repository
public interface ExportRequestRepository extends JpaRepository<ExportRequest, Long> {

    Optional<ExportRequest> findByExportId(String exportId);

    List<ExportRequest> findByUserOrderByCreatedAtDesc(User user);

    Page<ExportRequest> findByUserOrderByCreatedAtDesc(User user, Pageable pageable);

    List<ExportRequest> findByExportStatus(ExportRequest.ExportStatus status);

    @Query("SELECT er FROM ExportRequest er WHERE er.user = :user AND er.exportStatus = :status ORDER BY er.createdAt DESC")
    List<ExportRequest> findByUserAndStatus(@Param("user") User user, 
                                          @Param("status") ExportRequest.ExportStatus status);

    @Query("SELECT er FROM ExportRequest er WHERE er.createdAt < :cutoffDate AND er.exportStatus IN :statuses")
    List<ExportRequest> findOldRequests(@Param("cutoffDate") LocalDateTime cutoffDate, 
                                       @Param("statuses") List<ExportRequest.ExportStatus> statuses);

    @Query("SELECT COUNT(er) FROM ExportRequest er WHERE er.user = :user AND er.exportStatus = :status")
    long countByUserAndStatus(@Param("user") User user, 
                             @Param("status") ExportRequest.ExportStatus status);

    @Query("SELECT COUNT(er) FROM ExportRequest er WHERE er.user = :user AND er.createdAt BETWEEN :startDate AND :endDate")
    long countByUserAndDateRange(@Param("user") User user, 
                                @Param("startDate") LocalDateTime startDate, 
                                @Param("endDate") LocalDateTime endDate);

    boolean existsByExportId(String exportId);

    void deleteByExportStatusAndCreatedAtBefore(ExportRequest.ExportStatus status, LocalDateTime cutoffDate);

    @Query("SELECT er FROM ExportRequest er WHERE er.exportStatus = 'IN_PROGRESS' AND er.createdAt < :timeout")
    List<ExportRequest> findStuckRequests(@Param("timeout") LocalDateTime timeout);
}
"""
        },
        
        {
            "path": "src\\main\\java\\com\\anuj\\redditmessagemanager\\dto\\ExportRequestDTO.java",
            "content": """package com.anuj.redditmessagemanager.dto;

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
"""
        }
    ]
    
    # Additional DTO for upload responses
    upload_dto = {
        "path": "src\\main\\java\\com\\anuj\\redditmessagemanager\\dto\\UploadResponseDTO.java",
        "content": """package com.anuj.redditmessagemanager.dto;

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
"""
    }
    
    java_files.append(upload_dto)
    
    # Function to create files
    def create_files(files_list):
        print("\nCreating missing Java files...")
        
        for file_info in files_list:
            full_file_path = os.path.join(base_path, file_info["path"])
            
            try:
                # Create directory if it doesn't exist
                os.makedirs(os.path.dirname(full_file_path), exist_ok=True)
                
                # Create file (overwrite if exists)
                with open(full_file_path, 'w', encoding='utf-8') as f:
                    f.write(file_info["content"])
                print(f"✅ Created: {file_info['path']}")
                
            except Exception as e:
                print(f"❌ Failed to create {file_info['path']}: {str(e)}")
    
    # Create all Java files
    create_files(java_files)
    
    print("\n" + "="*70)
    print("✅ Missing Java files created successfully!")
    print("="*70)
    
    print("\nCreated Java Files:")
    print("✅ UploadController.java - File upload handling")
    print("✅ UploadService.java - File upload business logic")
    print("✅ ExportRequest.java - Export request entity")
    print("✅ ExportRequestRepository.java - Export data access")
    print("✅ ExportRequestDTO.java - Export data transfer object")
    print("✅ UploadResponseDTO.java - Upload response object")

if __name__ == "__main__":
    create_missing_java_files()