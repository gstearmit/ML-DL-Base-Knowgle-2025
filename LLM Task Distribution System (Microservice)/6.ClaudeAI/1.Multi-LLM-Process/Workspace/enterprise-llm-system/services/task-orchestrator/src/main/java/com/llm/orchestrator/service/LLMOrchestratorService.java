package com.llm.orchestrator.service;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.redis.core.RedisTemplate;
import org.springframework.kafka.core.KafkaTemplate;
import org.springframework.stereotype.Service;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import java.util.concurrent.TimeUnit;

@Service
@Slf4j
public class LLMOrchestratorService {

    @Autowired
    private TaskAnalyzer taskAnalyzer;
    
    @Autowired
    private KafkaTemplate<String, TaskRequest> kafkaTemplate;
    
    @Autowired
    private RedisTemplate<String, TaskMetadata> redisTemplate;

    public void orchestrateTask(TaskRequest request) {
        log.info("Orchestrating task: {}", request.getTaskId());
        
        // Analyze task requirements
        TaskAnalysis analysis = taskAnalyzer.analyze(request);
        
        // Store metadata in Redis
        redisTemplate.opsForValue().set(
            "task:" + request.getTaskId(),
            new TaskMetadata(analysis),
            1,
            TimeUnit.HOURS
        );
        
        // Route to appropriate queues
        for (SubTask subTask : analysis.getSubTasks()) {
            String routingKey = determineRoutingKey(subTask);
            kafkaTemplate.send(routingKey, subTask);
        }
    }
} 