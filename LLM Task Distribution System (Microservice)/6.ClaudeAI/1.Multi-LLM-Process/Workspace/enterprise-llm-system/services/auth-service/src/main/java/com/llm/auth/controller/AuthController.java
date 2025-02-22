package com.llm.auth.controller;

import com.llm.auth.model.AuthResult;
import com.llm.auth.service.AuthenticationService;
import lombok.extern.slf4j.Slf4j;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api/auth")
@Slf4j
public class AuthController {
    private final AuthenticationService authenticationService;

    public AuthController(AuthenticationService authenticationService) {
        this.authenticationService = authenticationService;
    }

    @PostMapping("/login")
    public ResponseEntity<AuthResult> login(
        @RequestParam String username, 
        @RequestParam String password
    ) {
        log.info("Login attempt for user: {}", username);
        AuthResult authResult = authenticationService.authenticate(username, password);
        
        if (authResult.getError() != null) {
            log.error("Authentication failed for user: {}", username);
            return ResponseEntity.badRequest().body(authResult);
        }
        
        log.info("User authenticated successfully: {}", username);
        return ResponseEntity.ok(authResult);
    }
}