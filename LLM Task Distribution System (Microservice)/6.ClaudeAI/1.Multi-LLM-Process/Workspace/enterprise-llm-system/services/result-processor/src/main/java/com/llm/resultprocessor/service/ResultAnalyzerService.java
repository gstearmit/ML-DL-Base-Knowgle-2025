package com.llm.resultprocessor.service;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import java.util.List;
import java.util.Map;
import java.util.HashMap;

@Service
@Slf4j
public class ResultAnalyzerService {

    @Autowired
    private ResultRepository resultRepository;
    
    @Autowired
    private QualityAnalyzer qualityAnalyzer;

    public AnalyzedResult analyzeResults(List<LLMResult> results) {
        log.info("Analyzing {} results", results.size());
        
        AnalyzedResult analyzedResult = new AnalyzedResult();
        
        // Calculate quality metrics
        Map<String, QualityMetrics> qualityScores = new HashMap<>();
        for (LLMResult result : results) {
            QualityMetrics metrics = qualityAnalyzer.analyze(result);
            qualityScores.put(result.getModel(), metrics);
        }
        
        // Select best result based on quality
        LLMResult bestResult = selectBestResult(results, qualityScores);
        analyzedResult.setBestResult(bestResult);
        analyzedResult.setQualityScores(qualityScores);
        
        return analyzedResult;
    }
} 