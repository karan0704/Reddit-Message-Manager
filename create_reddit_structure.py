import os

def create_reddit_message_manager_structure():
    # Base path from your provided path
    base_path = "D:\\Karan Ticket Project\\Reddit Message Manager"

    # Define the complete directory structure
    directories = [
        # Main Java package structure
        "src\\main\\java\\com\\anuj\\redditmessagemanager\\controller",
        "src\\main\\java\\com\\anuj\\redditmessagemanager\\entity",
        "src\\main\\java\\com\\anuj\\redditmessagemanager\\repository",
        "src\\main\\java\\com\\anuj\\redditmessagemanager\\service",
        "src\\main\\java\\com\\anuj\\redditmessagemanager\\config",
        "src\\main\\java\\com\\anuj\\redditmessagemanager\\dto",
        "src\\main\\java\\com\\anuj\\redditmessagemanager\\util",

        # Test directories
        "src\\test\\java\\com\\anuj\\redditmessagemanager",
        "src\\test\\java\\com\\anuj\\redditmessagemanager\\controller",
        "src\\test\\java\\com\\anuj\\redditmessagemanager\\service",

        # Resources directories
        "src\\main\\resources\\static\\css",
        "src\\main\\resources\\static\\js",
        "src\\main\\resources\\static\\images",
        "src\\main\\resources\\templates",
        "src\\test\\resources",

        # Additional useful directories
        "docs",
        "scripts",
        "logs"
    ]

    # Create directories
    print("Creating directory structure for Reddit Message Manager...")

    for directory in directories:
        full_path = os.path.join(base_path, directory)
        try:
            os.makedirs(full_path, exist_ok=True)
            print(f"✓ Created: {directory}")
        except Exception as e:
            print(f"✗ Failed to create {directory}: {str(e)}")

    # Create essential files with basic content
    files_to_create = [
        # Main application class (if not exists)
        {
            "path": "src\\main\\java\\com\\anuj\\redditmessagemanager\\RedditMessageManagerApplication.java",
            "content": """package com.anuj.redditmessagemanager;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication
public class RedditMessageManagerApplication {

    public static void main(String[] args) {
        SpringApplication.run(RedditMessageManagerApplication.class, args);
    }

}
"""
        },

        # Application properties template
        {
            "path": "src\\main\\resources\\application.properties",
            "content": """# MySQL Database Configuration
spring.datasource.url=jdbc:mysql://localhost:3306/reddit_messages
spring.datasource.username=root
spring.datasource.password=yourpassword
spring.datasource.driver-class-name=com.mysql.cj.jdbc.Driver

# JPA/Hibernate Configuration
spring.jpa.hibernate.ddl-auto=update
spring.jpa.show-sql=true
spring.jpa.properties.hibernate.dialect=org.hibernate.dialect.MySQL8Dialect
spring.jpa.properties.hibernate.format_sql=true

# Server Configuration
server.port=8080

# Session Configuration
server.servlet.session.timeout=30m
server.servlet.session.cookie.name=REDDIT_SESSION

# Reddit API Configuration
reddit.client.id=M9IRnasjoRFskVNj180eZA
reddit.client.secret=XDuQGOZ2yzaQoOaSKyAOguMkaWt6Cg
reddit.redirect.uri=http://localhost:8080/auth/callback

# Logging
logging.level.com.anuj.redditmessagemanager=DEBUG
logging.level.org.springframework.web=DEBUG
"""
        },

        # Basic HTML template
        {
            "path": "src\\main\\resources\\templates\\index.html",
            "content": """<!DOCTYPE html>
<html lang="en" xmlns:th="http://www.thymeleaf.org">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Reddit Message Manager</title>
    <link rel="stylesheet" href="/css/style.css">
</head>
<body>
    <div class="container">
        <h1>Reddit Message Manager</h1>
        <div class="auth-section">
            <a href="/login" class="login-btn">Login with Reddit</a>
        </div>
    </div>
</body>
</html>
"""
        },

        # Basic CSS file
        {
            "path": "src\\main\\resources\\static\\css\\style.css",
            "content": """/* Reddit Message Manager Styles */
body {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    margin: 0;
    padding: 0;
    background-color: #f5f5f5;
}

.container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 20px;
}

h1 {
    color: #333;
    text-align: center;
    margin-bottom: 30px;
}

.login-btn {
    display: inline-block;
    background-color: #ff4500;
    color: white;
    padding: 12px 24px;
    text-decoration: none;
    border-radius: 5px;
    text-align: center;
    font-weight: bold;
}

.login-btn:hover {
    background-color: #e03d00;
}

.auth-section {
    text-align: center;
    margin: 30px 0;
}
"""
        },

        # Basic JavaScript file
        {
            "path": "src\\main\\resources\\static\\js\\app.js",
            "content": """// Reddit Message Manager JavaScript
console.log('Reddit Message Manager loaded');

// Function to load messages
async function loadMessages(type) {
    try {
        const response = await fetch(`/api/messages/${type}`);
        const data = await response.json();
        
        if (response.ok) {
            displayMessages(data);
        } else {
            console.error('Error loading messages:', data.error);
        }
    } catch (error) {
        console.error('Network error:', error);
    }
}

// Function to display messages
function displayMessages(data) {
    // Implementation will be added later
    console.log('Messages loaded:', data);
}
"""
        },

        # README file
        {
            "path": "README.md",
            "content": """# Reddit Message Manager

A Spring Boot application for managing Reddit messages with OAuth2 integration.

## Features
- Reddit OAuth2 Authentication
- Message Loading (Inbox, Unread, Sent)
- Message Search
- MySQL Database Integration

## Setup
1. Install MySQL and create database `reddit_messages`
2. Update `application.properties` with your database credentials
3. Run: `mvn spring-boot:run`

## Reddit App Configuration
- Client ID: M9IRnasjoRFskVNj180eZA
- Redirect URI: http://localhost:8080/auth/callback

## Technologies Used
- Spring Boot 3.x
- Spring Data JPA
- MySQL
- Lombok
- Thymeleaf
- Bootstrap (for UI)
"""
        }
    ]

    # Create files
    print("\nCreating essential files...")

    for file_info in files_to_create:
        full_file_path = os.path.join(base_path, file_info["path"])

        try:
            # Create directory if it doesn't exist
            os.makedirs(os.path.dirname(full_file_path), exist_ok=True)

            # Only create file if it doesn't exist (to avoid overwriting)
            if not os.path.exists(full_file_path):
                with open(full_file_path, 'w', encoding='utf-8') as f:
                    f.write(file_info["content"])
                print(f"✓ Created file: {file_info['path']}")
            else:
                print(f"○ File already exists: {file_info['path']}")

        except Exception as e:
            print(f"✗ Failed to create file {file_info['path']}: {str(e)}")

    print("\n" + "="*60)
    print("Reddit Message Manager project structure created successfully!")
    print("="*60)
    print(f"Project location: {base_path}")
    print("\nNext steps:")
    print("1. Open the project in your IDE")
    print("2. Update MySQL credentials in application.properties")
    print("3. Create entity classes (User, RedditMessage)")
    print("4. Create repository interfaces")
    print("5. Create service classes")
    print("6. Create controller classes")
    print("7. Run: mvn spring-boot:run")

if __name__ == "__main__":
    create_reddit_message_manager_structure()