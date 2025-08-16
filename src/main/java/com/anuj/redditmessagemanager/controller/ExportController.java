package com.anuj.redditmessagemanager.controller;

import com.anuj.redditmessagemanager.dto.ExportDto;
import com.anuj.redditmessagemanager.service.ExportService;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.core.io.Resource;
import org.springframework.http.HttpHeaders;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import jakarta.servlet.http.HttpSession;
import java.util.Map;

@RestController
@RequestMapping("/api/export")
public class ExportController {
    
    private static final Logger logger = LoggerFactory.getLogger(ExportController.class);
    
    @Autowired
    private ExportService exportService;
    
    /**
     * Export chats to file
     */
    @PostMapping("/chats")
    public ResponseEntity<?> exportChats(@RequestBody ExportDto exportRequest, HttpSession session) {
        try {
            String username = getCurrentUsername(session);
            ExportDto exportResult = exportService.exportChats(username, exportRequest);
            
            return ResponseEntity.ok(Map.of(
                "success", true,
                "export", exportResult,
                "message", "Export started successfully"
            ));
            
        } catch (Exception e) {
            logger.error("Error starting export: {}", e.getMessage());
            return ResponseEntity.status(500).body(Map.of(
                "error", "Export failed: " + e.getMessage()
            ));
        }
    }
    
    /**
     * Download exported file
     */
    @GetMapping("/download/{filename}")
    public ResponseEntity<Resource> downloadExportedFile(@PathVariable String filename, HttpSession session) {
        try {
            String username = getCurrentUsername(session);
            Resource file = exportService.getExportedFile(username, filename);
            
            return ResponseEntity.ok()
                    .contentType(MediaType.APPLICATION_OCTET_STREAM)
                    .header(HttpHeaders.CONTENT_DISPOSITION, "attachment; filename=" + filename + """)
                    .body(file);
                    
        } catch (Exception e) {
            logger.error("Error downloading file: {}", e.getMessage());
            return ResponseEntity.notFound().build();
        }
    }
    
    /**
     * Get export status
     */
    @GetMapping("/status/{exportId}")
    public ResponseEntity<?> getExportStatus(@PathVariable String exportId, HttpSession session) {
        try {
            String username = getCurrentUsername(session);
            ExportDto status = exportService.getExportStatus(username, exportId);
            
            return ResponseEntity.ok(status);
            
        } catch (Exception e) {
            logger.error("Error getting export status: {}", e.getMessage());
            return ResponseEntity.status(500).body(Map.of(
                "error", "Failed to get export status: " + e.getMessage()
            ));
        }
    }
    
    private String getCurrentUsername(HttpSession session) {
        String username = (String) session.getAttribute("username");
        if (username == null) {
            throw new RuntimeException("User not authenticated");
        }
        return username;
    }
}
