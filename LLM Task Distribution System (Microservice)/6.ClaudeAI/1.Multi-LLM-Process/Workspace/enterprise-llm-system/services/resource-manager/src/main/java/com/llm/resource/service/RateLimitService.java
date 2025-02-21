package com.llm.resource.service;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.redis.core.RedisTemplate;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import java.util.concurrent.TimeUnit;

@Service
@Slf4j
public class RateLimitService {

    @Autowired
    private RedisTemplate<String, Integer> redisTemplate;
    
    @Value("${rate.limit.requests-per-minute}")
    private int requestsPerMinute;

    public boolean checkRateLimit(String userId) {
        String key = "rate:limit:" + userId;
        
        // Get current count
        Integer currentCount = redisTemplate.opsForValue().get(key);
        if (currentCount == null) {
            // First request in window
            redisTemplate.opsForValue().set(key, 1, 1, TimeUnit.MINUTES);
            return true;
        }
        
        if (currentCount >= requestsPerMinute) {
            log.warn("Rate limit exceeded for user: {}", userId);
            return false;
        }
        
        // Increment count
        redisTemplate.opsForValue().increment(key);
        return true;
    }
} 