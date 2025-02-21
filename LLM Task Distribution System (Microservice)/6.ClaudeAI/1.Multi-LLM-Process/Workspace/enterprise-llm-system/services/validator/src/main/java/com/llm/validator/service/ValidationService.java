package com.llm.validator.service;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.kafka.core.KafkaTemplate;
import org.springframework.stereotype.Service;

@Service
public class ValidationService {

    @Autowired
    private KafkaTemplate<String, ValidationMessage> kafkaTemplate;
    
    public ValidationResult validateTask(Task task) {
        // Validate task data
        ValidationResult result = new ValidationResult();
        
        if (isValid(task)) {
            // Send to Kafka for processing
            kafkaTemplate.send("task-validation", 
                new ValidationMessage(task.getTaskId(), "VALID"));
            result.setStatus("VALID");
        } else {
            result.setStatus("INVALID");
            result.setErrors(getValidationErrors(task));
        }
        
        return result;
    }
} 