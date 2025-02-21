package com.llm.resultprocessor.service;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.kafka.core.KafkaTemplate;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import lombok.extern.slf4j.Slf4j;
import java.util.UUID;
import java.util.List;
import java.util.Map;
import java.util.HashMap;

@Service
@Slf4j
public class ResultMergeService {

    @Autowired
    private ResultRepository resultRepository;
    
    @Autowired
    private KafkaTemplate<String, ProcessedResult> kafkaTemplate;

    @Transactional
    public void mergeResults(UUID taskId, List<LLMResult> results) {
        log.info("Merging results for task: {}", taskId);
        
        ProcessedResult mergedResult = new ProcessedResult();
        mergedResult.setTaskId(taskId);
        
        // Combine results using weighted scoring
        Map<String, Double> confidenceScores = new HashMap<>();
        for (LLMResult result : results) {
            confidenceScores.put(
                result.getModel(), 
                calculateConfidence(result)
            );
        }
        
        // Select best result
        LLMResult bestResult = selectBestResult(results, confidenceScores);
        mergedResult.setSelectedResult(bestResult);
        mergedResult.setConfidenceScores(confidenceScores);
        
        // Save and publish
        resultRepository.save(mergedResult);
        kafkaTemplate.send("final-results", mergedResult);
    }
} 