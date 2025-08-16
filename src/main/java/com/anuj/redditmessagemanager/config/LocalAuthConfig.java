package com.anuj.redditmessagemanager.config;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.web.servlet.config.annotation.InterceptorRegistry;
import org.springframework.web.servlet.config.annotation.WebMvcConfigurer;

@Configuration
public class LocalAuthConfig implements WebMvcConfigurer {
    
    /**
     * Authentication interceptor for session-based local authentication
     */
    @Bean
    public LocalAuthInterceptor localAuthInterceptor() {
        return new LocalAuthInterceptor();
    }
    
    @Override
    public void addInterceptors(InterceptorRegistry registry) {
        registry.addInterceptor(localAuthInterceptor())
                .addPathPatterns("/api/**", "/dashboard", "/chat/**")
                .excludePathPatterns("/api/auth/**", "/login", "/", "/static/**");
    }
    
    /**
     * Session timeout configuration (24 hours)
     */
    @Bean
    public SessionConfig sessionConfig() {
        return new SessionConfig();
    }
    
    public static class SessionConfig {
        private final int sessionTimeoutSeconds = 86400; // 24 hours
        private final boolean rememberLastUser = true;
        
        public int getSessionTimeoutSeconds() {
            return sessionTimeoutSeconds;
        }
        
        public boolean isRememberLastUser() {
            return rememberLastUser;
        }
    }
    
    public static class LocalAuthInterceptor implements org.springframework.web.servlet.HandlerInterceptor {
        @Override
        public boolean preHandle(jakarta.servlet.http.HttpServletRequest request, 
                               jakarta.servlet.http.HttpServletResponse response, 
                               Object handler) throws Exception {
            
            String username = (String) request.getSession().getAttribute("username");
            if (username == null) {
                response.sendRedirect("/login");
                return false;
            }
            return true;
        }
    }
}
