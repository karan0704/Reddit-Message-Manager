package com.anuj.redditmessagemanager.controller;

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
