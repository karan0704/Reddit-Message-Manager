package com.anuj.redditmessagemanager.controller;

import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;

import jakarta.servlet.http.HttpSession;

@Controller
public class HomeController {
    
    /**
     * Home page
     */
    @GetMapping("/")
    public String index(@RequestParam(required = false) String message, 
                       Model model, 
                       HttpSession session) {
        
        // Check if user is already logged in
        String username = (String) session.getAttribute("reddit_username");
        if (username != null) {
            return "redirect:/dashboard";
        }
        
        if (message != null) {
            model.addAttribute("message", message);
        }
        
        return "index";
    }
    
    /**
     * Dashboard page (requires authentication)
     */
    @GetMapping("/dashboard")
    public String dashboard(Model model, HttpSession session) {
        Long userId = (Long) session.getAttribute("user_id");
        String username = (String) session.getAttribute("reddit_username");
        
        if (userId == null || username == null) {
            return "redirect:/login";
        }
        
        model.addAttribute("username", username);
        model.addAttribute("userId", userId);
        
        return "dashboard";
    }
    
    /**
     * Messages page
     */
    @GetMapping("/messages")
    public String messages(Model model, HttpSession session) {
        Long userId = (Long) session.getAttribute("user_id");
        String username = (String) session.getAttribute("reddit_username");
        
        if (userId == null || username == null) {
            return "redirect:/login";
        }
        
        model.addAttribute("username", username);
        return "messages";
    }
    
    /**
     * Search page
     */
    @GetMapping("/search")
    public String search(Model model, HttpSession session) {
        Long userId = (Long) session.getAttribute("user_id");
        String username = (String) session.getAttribute("reddit_username");
        
        if (userId == null || username == null) {
            return "redirect:/login";
        }
        
        model.addAttribute("username", username);
        return "search";
    }
    
    /**
     * Error page
     */
    @GetMapping("/error")
    public String error(@RequestParam(required = false) String message, Model model) {
        if (message != null) {
            model.addAttribute("errorMessage", message);
        } else {
            model.addAttribute("errorMessage", "An unexpected error occurred");
        }
        
        return "error";
    }
    
    /**
     * About page
     */
    @GetMapping("/about")
    public String about() {
        return "about";
    }
}
