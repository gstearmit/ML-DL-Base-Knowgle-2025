package com.llm.auth.client;

import com.llm.auth.model.TokenInfo;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.*;
import org.springframework.stereotype.Component;
import org.springframework.util.LinkedMultiValueMap;
import org.springframework.util.MultiValueMap;
import org.springframework.web.client.RestTemplate;

@Component
public class KeycloakClient {
    private final RestTemplate restTemplate;
    private final String keycloakUrl;
    private final String realm;
    private final String clientId;
    private final String clientSecret;

    public KeycloakClient(
            @Value("${keycloak.auth-server-url}") String keycloakUrl,
            @Value("${keycloak.realm}") String realm,
            @Value("${keycloak.client-id}") String clientId,
            @Value("${keycloak.client-secret}") String clientSecret
    ) {
        this.restTemplate = new RestTemplate();
        this.keycloakUrl = keycloakUrl;
        this.realm = realm;
        this.clientId = clientId;
        this.clientSecret = clientSecret;
    }

    public TokenInfo getToken(String username, String password) {
        String tokenUrl = String.format("%s/realms/%s/protocol/openid-connect/token", keycloakUrl, realm);

        HttpHeaders headers = new HttpHeaders();
        headers.setContentType(MediaType.APPLICATION_FORM_URLENCODED);

        MultiValueMap<String, String> map = new LinkedMultiValueMap<>();
        map.add("grant_type", "password");
        map.add("client_id", clientId);
        map.add("client_secret", clientSecret);
        map.add("username", username);
        map.add("password", password);

        HttpEntity<MultiValueMap<String, String>> request = new HttpEntity<>(map, headers);

        ResponseEntity<TokenInfo> response = restTemplate.postForEntity(
                tokenUrl,
                request,
                TokenInfo.class
        );

        return response.getBody();
    }

    public TokenInfo refreshToken(String refreshToken) {
        String tokenUrl = String.format("%s/realms/%s/protocol/openid-connect/token", keycloakUrl, realm);

        HttpHeaders headers = new HttpHeaders();
        headers.setContentType(MediaType.APPLICATION_FORM_URLENCODED);

        MultiValueMap<String, String> map = new LinkedMultiValueMap<>();
        map.add("grant_type", "refresh_token");
        map.add("client_id", clientId);
        map.add("client_secret", clientSecret);
        map.add("refresh_token", refreshToken);

        HttpEntity<MultiValueMap<String, String>> request = new HttpEntity<>(map, headers);

        ResponseEntity<TokenInfo> response = restTemplate.postForEntity(
                tokenUrl,
                request,
                TokenInfo.class
        );

        return response.getBody();
    }

    public void logout(String token) {
        String logoutUrl = String.format("%s/realms/%s/protocol/openid-connect/logout", keycloakUrl, realm);

        HttpHeaders headers = new HttpHeaders();
        headers.setContentType(MediaType.APPLICATION_FORM_URLENCODED);

        MultiValueMap<String, String> map = new LinkedMultiValueMap<>();
        map.add("client_id", clientId);
        map.add("client_secret", clientSecret);
        map.add("refresh_token", token);

        HttpEntity<MultiValueMap<String, String>> request = new HttpEntity<>(map, headers);

        restTemplate.postForEntity(logoutUrl, request, Void.class);
    }
}
