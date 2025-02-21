package com.llm.auth.store;

import com.llm.auth.model.TokenInfo;
import org.springframework.data.redis.core.RedisTemplate;
import org.springframework.stereotype.Component;

import java.util.concurrent.TimeUnit;

@Component
public class TokenStore {
    private final RedisTemplate<String, TokenInfo> redisTemplate;
    private static final String KEY_PREFIX = "token:";

    public TokenStore(RedisTemplate<String, TokenInfo> redisTemplate) {
        this.redisTemplate = redisTemplate;
    }

    public void storeToken(String userId, TokenInfo tokenInfo) {
        String key = KEY_PREFIX + userId;
        redisTemplate.opsForValue().set(key, tokenInfo, tokenInfo.getExpiresIn(), TimeUnit.SECONDS);
    }

    public TokenInfo getToken(String userId) {
        String key = KEY_PREFIX + userId;
        return redisTemplate.opsForValue().get(key);
    }

    public void removeToken(String userId) {
        String key = KEY_PREFIX + userId;
        redisTemplate.delete(key);
    }
} 