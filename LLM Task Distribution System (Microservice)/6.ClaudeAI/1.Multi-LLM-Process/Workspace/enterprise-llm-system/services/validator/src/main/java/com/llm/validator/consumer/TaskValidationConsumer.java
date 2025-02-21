package com.llm.validator.consumer;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.kafka.annotation.KafkaListener;
import org.springframework.kafka.core.KafkaTemplate;
import org.springframework.stereotype.Service;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

@Service
@Slf4j
public class TaskValidationConsumer {

    @Autowired
    private ValidationService validationService;
    
    @Autowired
    private KafkaTemplate<String, Task> kafkaTemplate;

    @KafkaListener(topics = "task-validation", groupId = "validator-group")
    public void consume(Task task) {
        log.info("Received task for validation: {}", task.getTaskId());
        
        ValidationResult result = validationService.validateTask(task);
        
        if (result.getStatus().equals("VALID")) {
            // Forward to LLM processing queue
            kafkaTemplate.send("llm-processing", task);
        } else {
            // Update task status to INVALID
            task.setStatus("INVALID");
            task.setErrorMessage(String.join(", ", result.getErrors()));
            kafkaTemplate.send("task-status-update", task);
        }
    }
} 