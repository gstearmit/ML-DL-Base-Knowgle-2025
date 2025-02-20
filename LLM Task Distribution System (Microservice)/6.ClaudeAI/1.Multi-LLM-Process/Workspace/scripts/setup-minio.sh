#!/bin/bash

# MinIO Setup Script for Enterprise LLM System
# This script initializes and configures MinIO for production use

set -e

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Log function
log() {
    echo -e "${GREEN}[$(date +'%Y-%m-%d %H:%M:%S')]${NC} $1"
}

# Error handling function
error_handler() {
    echo -e "${RED}Error occurred in script at line: ${BASH_LINENO[0]}${NC}"
    exit 1
}

trap error_handler ERR

# Install MinIO Client
install_mc() {
    log "Installing MinIO Client..."
    curl -O https://dl.min.io/client/mc/release/linux-amd64/mc
    chmod +x mc
    sudo mv mc /usr/local/bin/
    
    # Verify installation
    if ! mc --version; then
        echo -e "${RED}Failed to install MinIO Client${NC}"
        exit 1
    fi
}

# Check if Docker is running
check_docker() {
    log "Checking Docker status..."
    if ! docker info >/dev/null 2>&1; then
        echo -e "${RED}Docker is not running. Please start Docker first.${NC}"
        exit 1
    fi
}

# Check for required commands
check_requirements() {
    log "Checking required commands..."
    for cmd in docker curl openssl; do
        if ! command -v $cmd >/dev/null 2>&1; then
            echo -e "${RED}Error: Required command '$cmd' is not installed.${NC}"
            exit 1
        fi
    done

    # Check for MinIO Client and install if missing
    if ! command -v mc >/dev/null 2>&1; then
        install_mc
    fi
}

# Create necessary directories
setup_directories() {
    log "Creating MinIO directories..."
    mkdir -p ./data/minio/data ./data/minio/config ./configs/minio
    chmod 700 ./data/minio/data
    chmod 700 ./data/minio/config
}

# Generate MinIO configuration
generate_config() {
    log "Generating MinIO configuration..."
    mkdir -p ./configs/minio

    # Generate secure password if not provided
    MINIO_ROOT_USER=${MINIO_ROOT_USER:-admin}
    MINIO_ROOT_PASSWORD=${MINIO_ROOT_PASSWORD:-$(openssl rand -base64 32)}

    cat > ./configs/minio/config.env << EOL
MINIO_ROOT_USER=${MINIO_ROOT_USER}
MINIO_ROOT_PASSWORD=${MINIO_ROOT_PASSWORD}
MINIO_REGION=${MINIO_REGION:-us-east-1}
MINIO_BROWSER=${MINIO_BROWSER:-on}
MINIO_PROMETHEUS_AUTH_TYPE=public
MINIO_COMPRESSION=on
MINIO_COMPRESSION_EXTENSIONS=.txt,.log,.csv,.json,.tar,.xml,.bin
MINIO_COMPRESSION_MIME_TYPES=text/*,application/json,application/xml
MINIO_DOMAIN=${MINIO_DOMAIN:-localhost}
EOL

    # Export credentials for mc client
    export MINIO_ROOT_USER
    export MINIO_ROOT_PASSWORD
}

# Create necessary buckets and policies
initialize_buckets() {
    log "Initializing MinIO buckets..."
    
    # Wait for MinIO to be ready
    until curl --silent --fail http://localhost:9000/minio/health/ready; do
        echo -n "."
        sleep 1
    done
    
    # Remove existing alias if present
    mc alias remove local >/dev/null 2>&1 || true
    
    # Create required buckets
    mc alias set local http://localhost:9000 "${MINIO_ROOT_USER}" "${MINIO_ROOT_PASSWORD}"
    
    # Verify connection
    mc admin info local || {
        echo -e "${RED}Failed to authenticate with MinIO server${NC}"
        exit 1
    }
    
    # Create buckets with versioning enabled
    for bucket in "llm-data" "model-cache" "user-data" "system-backup"; do
        mc mb "local/${bucket}" --ignore-existing
        mc version enable "local/${bucket}"
        mc encrypt set sse-s3 "local/${bucket}"
    done
}

# Configure MinIO policies
setup_policies() {
    log "Setting up MinIO policies..."
    
    # Create read-only policy
    cat > ./configs/minio/readonly-policy.json << EOL
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "s3:GetObject",
                "s3:ListBucket"
            ],
            "Resource": [
                "arn:aws:s3:::llm-data/*",
                "arn:aws:s3:::model-cache/*"
            ]
        }
    ]
}
EOL

    # Create read-write policy
    cat > ./configs/minio/readwrite-policy.json << EOL
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "s3:GetObject",
                "s3:PutObject",
                "s3:ListBucket",
                "s3:DeleteObject"
            ],
            "Resource": [
                "arn:aws:s3:::llm-data/*",
                "arn:aws:s3:::user-data/*"
            ]
        }
    ]
}
EOL

    # Apply policies
    mc admin policy create local readonly-policy ./configs/minio/readonly-policy.json
    mc admin policy create local readwrite-policy ./configs/minio/readwrite-policy.json
}

# Configure backup settings
setup_backups() {
    log "Configuring MinIO backup settings..."
    
    cat > ./configs/minio/backup-config.json << EOL
{
    "backup": {
        "schedule": "0 0 * * *",
        "retention": {
            "days": 30
        },
        "destination": "local/system-backup"
    }
}
EOL
}

# Configure monitoring
setup_monitoring() {
    log "Setting up MinIO monitoring..."
    
    mkdir -p ./configs/prometheus
    
    # Configure Prometheus endpoints
    mc admin prometheus generate local > ./configs/prometheus/minio-metrics.yml
    
    # Configure audit logging if token is provided
    if [ ! -z "${ELASTIC_TOKEN}" ]; then
        mc admin config set local audit endpoint=http://elasticsearch:9200 auth_token=${ELASTIC_TOKEN}
    fi
}

# Main execution
main() {
    log "Starting MinIO setup..."
    
    check_requirements
    check_docker
    setup_directories
    generate_config
    
    # Start MinIO service
    log "Starting MinIO service..."
    docker-compose up -d minio
    
    # Wait for service to be ready
    sleep 10
    
    initialize_buckets
    setup_policies
    setup_backups
    setup_monitoring
    
    log "Verifying setup..."
    if mc admin info local >/dev/null 2>&1; then
        echo -e "${GREEN}MinIO setup completed successfully!${NC}"
    else
        echo -e "${RED}MinIO setup failed. Please check the logs.${NC}"
        exit 1
    fi
}

# Execute main function
main

# Display important information
echo -e "\n${YELLOW}Important Information:${NC}"
echo -e "MinIO Console: http://localhost:9001"
echo -e "Root User: ${MINIO_ROOT_USER}"
echo -e "Root Password: ${MINIO_ROOT_PASSWORD}"
echo -e "\nPlease save these credentials securely."