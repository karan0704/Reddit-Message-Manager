package com.anuj.redditmessagemanager.service;

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
