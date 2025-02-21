package com.llm.reliability.service;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Service;
import lombok.extern.slf4j.Slf4j;

@Service
@Slf4j
public class BackupService {

    @Autowired
    private MinioClient minioClient;
    
    @Autowired
    private DatabaseService databaseService;

    @Scheduled(cron = "0 0 */4 * * *") // Every 4 hours
    public void performBackup() {
        log.info("Starting scheduled backup");
        
        try {
            // Backup databases
            for (String database : databaseService.getDatabases()) {
                String backupFile = createDatabaseBackup(database);
                uploadToMinio(backupFile, "database-backups");
            }
            
            // Backup configurations
            backupConfigurations();
            
            // Backup metrics
            backupMetrics();
            
            log.info("Backup completed successfully");
        } catch (Exception e) {
            log.error("Backup failed", e);
            notifyAdmins("Backup failed: " + e.getMessage());
        }
    }
} 