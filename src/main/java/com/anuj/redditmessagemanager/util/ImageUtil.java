package com.anuj.redditmessagemanager.util;

import org.springframework.stereotype.Component;

import javax.imageio.ImageIO;
import java.awt.*;
import java.awt.image.BufferedImage;
import java.io.File;
import java.io.IOException;

@Component
public class ImageUtil {
    
    private static final int THUMBNAIL_SIZE = 150;
    private static final int MAX_IMAGE_WIDTH = 1920;
    private static final int MAX_IMAGE_HEIGHT = 1080;
    
    /**
     * Create thumbnail of image
     */
    public static String createThumbnail(String imagePath) throws IOException {
        File originalFile = new File("./uploads/" + imagePath);
        if (!originalFile.exists()) {
            throw new IOException("Original image not found");
        }
        
        BufferedImage originalImage = ImageIO.read(originalFile);
        if (originalImage == null) {
            throw new IOException("Cannot read image file");
        }
        
        // Calculate thumbnail dimensions
        int width = originalImage.getWidth();
        int height = originalImage.getHeight();
        
        double scale = Math.min((double) THUMBNAIL_SIZE / width, (double) THUMBNAIL_SIZE / height);
        int thumbnailWidth = (int) (width * scale);
        int thumbnailHeight = (int) (height * scale);
        
        // Create thumbnail
        BufferedImage thumbnail = new BufferedImage(thumbnailWidth, thumbnailHeight, BufferedImage.TYPE_INT_RGB);
        Graphics2D g2d = thumbnail.createGraphics();
        g2d.setRenderingHint(RenderingHints.KEY_INTERPOLATION, RenderingHints.VALUE_INTERPOLATION_BILINEAR);
        g2d.drawImage(originalImage, 0, 0, thumbnailWidth, thumbnailHeight, null);
        g2d.dispose();
        
        // Save thumbnail
        String thumbnailPath = imagePath.replace(".", "_thumb.");
        File thumbnailFile = new File("./uploads/" + thumbnailPath);
        ImageIO.write(thumbnail, "jpg", thumbnailFile);
        
        return thumbnailPath;
    }
    
    /**
     * Resize image if too large
     */
    public static String resizeIfNeeded(String imagePath) throws IOException {
        File originalFile = new File("./uploads/" + imagePath);
        BufferedImage originalImage = ImageIO.read(originalFile);
        
        if (originalImage == null) {
            return imagePath;
        }
        
        int width = originalImage.getWidth();
        int height = originalImage.getHeight();
        
        // Check if resize is needed
        if (width <= MAX_IMAGE_WIDTH && height <= MAX_IMAGE_HEIGHT) {
            return imagePath;
        }
        
        // Calculate new dimensions
        double scale = Math.min((double) MAX_IMAGE_WIDTH / width, (double) MAX_IMAGE_HEIGHT / height);
        int newWidth = (int) (width * scale);
        int newHeight = (int) (height * scale);
        
        // Resize image
        BufferedImage resizedImage = new BufferedImage(newWidth, newHeight, BufferedImage.TYPE_INT_RGB);
        Graphics2D g2d = resizedImage.createGraphics();
        g2d.setRenderingHint(RenderingHints.KEY_INTERPOLATION, RenderingHints.VALUE_INTERPOLATION_BILINEAR);
        g2d.drawImage(originalImage, 0, 0, newWidth, newHeight, null);
        g2d.dispose();
        
        // Save resized image
        String resizedPath = imagePath.replace(".", "_resized.");
        File resizedFile = new File("./uploads/" + resizedPath);
        ImageIO.write(resizedImage, "jpg", resizedFile);
        
        // Delete original if different
        if (!resizedPath.equals(imagePath)) {
            originalFile.delete();
        }
        
        return resizedPath;
    }
    
    /**
     * Get image dimensions
     */
    public static Dimension getImageDimensions(String imagePath) throws IOException {
        File imageFile = new File("./uploads/" + imagePath);
        BufferedImage image = ImageIO.read(imageFile);
        
        if (image == null) {
            throw new IOException("Cannot read image file");
        }
        
        return new Dimension(image.getWidth(), image.getHeight());
    }
    
    /**
     * Check if image is valid
     */
    public static boolean isValidImage(String imagePath) {
        try {
            File imageFile = new File("./uploads/" + imagePath);
            BufferedImage image = ImageIO.read(imageFile);
            return image != null;
        } catch (IOException e) {
            return false;
        }
    }
}
