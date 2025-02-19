#!/bin/bash

# Enterprise Database Backup Script
# This script performs backups of PostgreSQL databases, Redis data, and other persistent storage

set -e

# Load environment variables
source .env

# Configuration
BACKUP_DIR="/backup"
DATE=$(date +%Y%m%d_%H%M%S)
RETENTION_DAYS=30
LOG_FILE="/var/log/db-backup.log"

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Logging function
log() {
    echo -e "[$(date +'%Y-%m-%d %H:%M:%S')] $1" | tee -a $LOG_FILE
}

# Error handling
error_handler() {
    log "${RED}Error occurred in script at line: ${BASH_LINENO[0]}${NC}"
    # Send alert to monitoring system
    curl -X POST http://localhost:9093/api/v1/alerts \
        -H 'Content-Type: application/json' \
        -d "{\"status\": \"firing\", \"labels\": {\"alertname\": \"BackupFailure\", \"severity\": \"critical\"}}"
    exit 1
}

trap error_handler ERR

# Create backup directory structure
setup_backup_dir() {
    log "${GREEN}Setting up backup directory structure...${NC}"
    mkdir -p ${BACKUP_DIR}/{postgres,redis,minio}
    chmod 700 ${BACKUP_DIR}
}

# PostgreSQL backup function
backup_postgres() {
    log "${GREEN}Starting PostgreSQL backup...${NC}"
    
    # Get list of databases
    databases=$(docker exec postgres psql -U ${POSTGRES_USER} -t -c "SELECT datname FROM pg_database WHERE datistemplate = false;")
    
    for db in $databases; do
        backup_file="${BACKUP_DIR}/postgres/${db}_${DATE}.sql.gz"
        log "Backing up database: $db"
        
        # Perform backup with progress monitoring
        docker exec postgres pg_dump -U ${POSTGRES_USER} -d $db \
            | pv -p -t -e -N "Backing up $db" \
            | gzip > $backup_file
        
        # Verify backup integrity
        if gunzip -t $backup_file >/dev/null 2>&1; then
            log "${GREEN}✓ Successfully backed up $db${NC}"
        else
            log "${RED}× Backup verification failed for $db${NC}"
            error_handler
        fi
    done
}

# Redis backup function
backup_redis() {
    log "${GREEN}Starting Redis backup...${NC}"
    backup_file="${BACKUP_DIR}/redis/redis_${DATE}.rdb.gz"
    
    # Trigger Redis save
    docker exec redis redis-cli SAVE
    
    # Copy and compress dump.rdb
    docker cp redis:/data/dump.rdb - \
        | pv -p -t -e -N "Backing up Redis" \
        | gzip > $backup_file
    
    # Verify backup
    if gunzip -t $backup_file >/dev/null 2>&1; then
        log "${GREEN}✓ Successfully backed up Redis${NC}"
    else
        log "${RED}× Redis backup verification failed${NC}"
        error_handler
    fi
}

# MinIO backup function
backup_minio() {
    log "${GREEN}Starting MinIO backup...${NC}"
    backup_file="${BACKUP_DIR}/minio/minio_${DATE}.tar.gz"
    
    # Use mc to backup MinIO buckets
    for bucket in "llm-data" "model-cache" "user-data"; do
        log "Backing up bucket: $bucket"
        mc mirror local/$bucket ${BACKUP_DIR}/minio/$bucket
    done
    
    # Create compressed archive
    tar -czf $backup_file -C ${BACKUP_DIR}/minio .
    
    # Verify backup
    if tar -tzf $backup_file >/dev/null 2>&1; then
        log "${GREEN}✓ Successfully backed up MinIO buckets${NC}"
    else
        log "${RED}× MinIO backup verification failed${NC}"
        error_handler
    fi
}

# Upload backups to remote storage
upload_backups() {
    log "${GREEN}Uploading backups to remote storage...${NC}"
    
    # Configure MinIO client
    mc alias set backup-store ${MINIO_ENDPOINT} ${MINIO_ROOT_USER} ${MINIO_ROOT_PASSWORD}
    
    # Upload with progress monitoring
    find ${BACKUP_DIR} -type f -name "*.gz" | while read file; do
        relative_path=${file#${BACKUP_DIR}/}
        log "Uploading: $relative_path"
        mc cp --progress $file backup-store/system-backup/${DATE}/$relative_path
    done
}

# Cleanup old backups
cleanup_old_backups() {
    log "${YELLOW}Cleaning up old backups...${NC}"
    
    # Local cleanup
    find ${BACKUP_DIR} -type f -mtime +${RETENTION_DAYS} -delete
    
    # Remote cleanup
    mc rm --recursive --force --older-than ${RETENTION_DAYS}d backup-store/system-backup/
}

# Backup verification
verify_backups() {
    log "${GREEN}Verifying backup integrity...${NC}"
    
    # Check backup sizes
    find ${BACKUP_DIR} -type f -name "*.gz" | while read file; do
        size=$(du -h "$file" | cut -f1)
        log "Backup size for $(basename $file): $size"
        
        # Alert if backup is suspiciously small
        if [[ $(stat -f%z "$file") -lt 1024 ]]; then
            log "${RED}Warning: Backup file $file is suspiciously small${NC}"
        fi
    done
    
    # Verify remote upload
    mc ls backup-store/system-backup/${DATE}/ >/dev/null 2>&1 || {
        log "${RED}Remote backup verification failed${NC}"
        error_handler
    }
}

# Main execution
main() {
    log "${GREEN}Starting database backup process...${NC}"
    
    setup_backup_dir
    backup_postgres
    backup_redis
    backup_minio
    upload_backups
    verify_backups
    cleanup_old_backups
    
    log "${GREEN}Backup process completed successfully!${NC}"
    
    # Generate backup report
    cat << EOF > ${BACKUP_DIR}/backup_report_${DATE}.txt
Backup Summary Report
===================
Date: $(date)
Status: Success
Backup Location: ${BACKUP_DIR}
Remote Storage: ${MINIO_ENDPOINT}/system-backup

Databases Backed Up:
$(find ${BACKUP_DIR} -type f -name "*.gz" | while read file; do
    echo "- $(basename $file): $(du -h $file | cut -f1)"
done)

Retention Policy: ${RETENTION_DAYS} days
EOF
}

# Execute main function
main

# Send success notification
curl -X POST http://localhost:9093/api/v1/alerts \
    -H 'Content-Type: application/json' \
    -d "{\"status\": \"resolved\", \"labels\": {\"alertname\": \"BackupSuccess\", \"severity\": \"info\"}}"