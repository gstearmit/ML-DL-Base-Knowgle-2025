package com.llm.dataprocessor.service;

import org.jsoup.Jsoup;
import org.jsoup.safety.Safelist;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

@Service
@Slf4j
public class DataSanitizerService {

    @Autowired
    private SchemaValidator schemaValidator;

    public SanitizedData sanitize(RawData rawData) {
        log.info("Sanitizing data for request: {}", rawData.getRequestId());
        
        // Remove potential XSS
        String sanitizedInput = Jsoup.clean(rawData.getInput(), Safelist.basic());
        
        // Validate against schema
        ValidationResult validation = schemaValidator.validate(sanitizedInput);
        if (!validation.isValid()) {
            throw new ValidationException(validation.getErrors());
        }
        
        // Transform to internal format
        return DataTransformer.transform(sanitizedInput);
    }
} 