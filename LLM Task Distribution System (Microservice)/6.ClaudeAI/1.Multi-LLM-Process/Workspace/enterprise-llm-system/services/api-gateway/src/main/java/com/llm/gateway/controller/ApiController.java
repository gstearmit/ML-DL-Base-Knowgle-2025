package com.llm.gateway.controller;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import lombok.extern.slf4j.Slf4j;

@RestController
@RequestMapping("/api")
@Slf4j
public class ApiController {

    @Autowired
    private AuthenticationService authService;
    
    @Autowired
    private TaskManagerClient taskManagerClient;

    @PostMapping("/tasks")
    public ResponseEntity<TaskResponse> createTask(
            @RequestHeader("Authorization") String token,
            @RequestBody TaskRequest request) {
        
        log.info("Received task creation request");
        
        // Step 1: Validate token
        AuthResult authResult = authService.validateToken(token);
        if (!authResult.isValid()) {
            throw new UnauthorizedException("Invalid token");
        }
        
        // Step 2: Forward to Task Manager
        request.setUserId(authResult.getUserId());
        TaskResponse response = taskManagerClient.createTask(request);
        
        return ResponseEntity.ok(response);
    }
} 