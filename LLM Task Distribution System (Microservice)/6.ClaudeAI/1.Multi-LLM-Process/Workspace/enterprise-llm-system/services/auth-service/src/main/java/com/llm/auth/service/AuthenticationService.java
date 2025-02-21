package com.llm.auth.service;

import com.llm.auth.client.KeycloakClient;
import com.llm.auth.model.AuthResult;
import com.llm.auth.model.TokenInfo;
import com.llm.auth.store.TokenStore;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;

@Service
@Slf4j
public class AuthenticationService {
    private final KeycloakClient keycloakClient;
    private final TokenStore tokenStore;

    public AuthenticationService(KeycloakClient keycloakClient, TokenStore tokenStore) {
        this.keycloakClient = keycloakClient;
        this.tokenStore = tokenStore;
    }

    public AuthResult authenticate(String username, String password) {
        try {
            TokenInfo tokenInfo = keycloakClient.getToken(username, password);
            tokenStore.storeToken(username, tokenInfo);

            return AuthResult.builder()
                    .accessToken(tokenInfo.getAccessToken())
                    .refreshToken(tokenInfo.getRefreshToken())
                    .expiresIn(tokenInfo.getExpiresIn())
                    .build();
        } catch (Exception e) {
            log.error("Authentication failed for user: {}", username, e);
            return AuthResult.builder()
                    .error("authentication_failed")
                    .errorDescription(e.getMessage())
                    .build();
        }
    }
} 