# Reddit Message Manager

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
