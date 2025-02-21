package com.llm.auth.model;

import lombok.Builder;
import lombok.Data;

@Data
@Builder
public class AuthResult {
    private String accessToken;
    private String refreshToken;
    private Long expiresIn;
    private String error;
    private String errorDescription;
} 