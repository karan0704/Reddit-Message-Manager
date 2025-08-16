package com.anuj.redditmessagemanager.util;

import org.springframework.stereotype.Component;
import org.springframework.web.multipart.MultipartFile;

import java.io.File;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.UUID;

@Component
public class FileUtil {
    
    private static final String UPLOAD_DIR = "./uploads/";
    private static final long MAX_FILE_SIZE = 10 * 1024 * 1024; // 10MB
    private static final String[] ALLOWED_IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".webp"};
    private static final String[] ALLOWED_FILE_EXTENSIONS = {".pdf", ".doc", ".docx", ".txt", ".zip"};
    
    /**
     * Save uploaded file
     */
    public static String saveFile(MultipartFile file, String directory) throws IOException {
        if (file.isEmpty()) {
            throw new IOException("File is empty");
        }
        
        if (file.getSize() > MAX_FILE_SIZE) {
            throw new IOException("File size exceeds maximum limit");
        }
        
        // Create directory if it doesn't exist
        Path uploadPath = Paths.get(UPLOAD_DIR + directory);
        Files.createDirectories(uploadPath);
        
        // Generate unique filename
        String originalFilename = file.getOriginalFilename();
        String extension = getFileExtension(originalFilename);
        String uniqueFilename = UUID.randomUUID().toString() + extension;
        
        // Save file
        Path filePath = uploadPath.resolve(uniqueFilename);
        Files.copy(file.getInputStream(), filePath);
        
        return directory + "/" + uniqueFilename;
    }
    
    /**
     * Get file extension
     */
    public static String getFileExtension(String filename) {
        if (filename == null || filename.isEmpty()) {
            return "";
        }
        
        int lastDot = filename.lastIndexOf('.');
        return lastDot > 0 ? filename.substring(lastDot).toLowerCase() : "";
    }
    
    /**
     * Check if file is an image
     */
    public static boolean isImageFile(String filename) {
        String extension = getFileExtension(filename);
        
        for (String allowedExt : ALLOWED_IMAGE_EXTENSIONS) {
            if (allowedExt.equals(extension)) {
                return true;
            }
        }
        
        return false;
    }
    
    /**
     * Check if file type is allowed
     */
    public static boolean isAllowedFileType(String filename) {
        String extension = getFileExtension(filename);
        
        // Check images
        for (String allowedExt : ALLOWED_IMAGE_EXTENSIONS) {
            if (allowedExt.equals(extension)) {
                return true;
            }
        }
        
        // Check other files
        for (String allowedExt : ALLOWED_FILE_EXTENSIONS) {
            if (allowedExt.equals(extension)) {
                return true;
            }
        }
        
        return false;
    }
    
    /**
     * Format file size for display
     */
    public static String formatFileSize(long bytes) {
        if (bytes < 1024) {
            return bytes + " B";
        } else if (bytes < 1024 * 1024) {
            return String.format("%.1f KB", bytes / 1024.0);
        } else if (bytes < 1024 * 1024 * 1024) {
            return String.format("%.1f MB", bytes / (1024.0 * 1024.0));
        } else {
            return String.format("%.1f GB", bytes / (1024.0 * 1024.0 * 1024.0));
        }
    }
    
    /**
     * Delete file
     */
    public static boolean deleteFile(String filePath) {
        try {
            Path path = Paths.get(UPLOAD_DIR + filePath);
            return Files.deleteIfExists(path);
        } catch (IOException e) {
            return false;
        }
    }
    
    /**
     * Check if file exists
     */
    public static boolean fileExists(String filePath) {
        Path path = Paths.get(UPLOAD_DIR + filePath);
        return Files.exists(path);
    }
}
