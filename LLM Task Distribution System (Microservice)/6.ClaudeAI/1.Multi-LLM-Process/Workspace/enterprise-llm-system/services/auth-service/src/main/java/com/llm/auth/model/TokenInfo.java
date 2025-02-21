package com.llm.auth.model;

import lombok.Builder;
import lombok.Data;

@Data
@Builder
public class TokenInfo {
    private String accessToken;
    private String refreshToken;
    private Long expiresIn;
    private String tokenType;
    private String scope;
} 