#!/bin/bash

# Enterprise Database Initialization Script
# This script initializes all databases and required schemas for the LLM processing system

set -e

# Load environment variables
source .env

# Configuration
mkdir -p ./logs
LOG_FILE="./logs/db-init.log"
SCHEMA_DIR="./configs/postgresql/schemas"

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
    exit 1
}

trap error_handler ERR

# PostgreSQL initialization
init_postgresql() {
    log "${GREEN}Initializing PostgreSQL databases...${NC}"
    
    # Wait for PostgreSQL to be ready
    until docker exec postgres pg_isready; do
        log "Waiting for PostgreSQL to be ready..."
        sleep 2
    done
    
    # Create databases
    for db in "keycloak" "kong" "taskdb" "resultdb" "accountdb"; do
        log "Creating database: $db"
        docker exec postgres psql -U ${POSTGRES_USER} -c "CREATE DATABASE $db;" || true
    done
    
    # Initialize schemas and extensions
    cat << EOF | docker exec -i postgres psql -U ${POSTGRES_USER}
    -- Task Management Schema
    \c taskdb
    CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
    CREATE SCHEMA IF NOT EXISTS task_management;
    
    CREATE TABLE IF NOT EXISTS task_management.tasks (
        id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
        task_type VARCHAR(50) NOT NULL,
        status VARCHAR(20) NOT NULL,
        priority INTEGER NOT NULL,
        created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
        metadata JSONB
    );
    
    CREATE INDEX IF NOT EXISTS idx_tasks_status ON task_management.tasks(status);
    CREATE INDEX IF NOT EXISTS idx_tasks_priority ON task_management.tasks(priority);
    
    -- Result Storage Schema
    \c resultdb
    CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
    CREATE EXTENSION IF NOT EXISTS "pgcrypto";
    CREATE SCHEMA IF NOT EXISTS result_storage;
    
    CREATE TABLE IF NOT EXISTS result_storage.results (
        id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
        task_id UUID NOT NULL,
        model_name VARCHAR(100) NOT NULL,
        result_data JSONB NOT NULL,
        confidence_score DECIMAL(5,4),
        processing_time INTEGER,
        created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
    );
    
    CREATE INDEX IF NOT EXISTS idx_results_task_id ON result_storage.results(task_id);
    
    -- Account Management Schema
    \c accountdb
    CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
    CREATE EXTENSION IF NOT EXISTS "pgcrypto";
    CREATE SCHEMA IF NOT EXISTS account_management;
    
    CREATE TABLE IF NOT EXISTS account_management.accounts (
        id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
        username VARCHAR(50) UNIQUE NOT NULL,
        email VARCHAR(255) UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        api_key UUID DEFAULT uuid_generate_v4(),
        rate_limit INTEGER DEFAULT 1000,
        created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
    );
    
    CREATE INDEX IF NOT EXISTS idx_accounts_username ON account_management.accounts(username);
    CREATE INDEX IF NOT EXISTS idx_accounts_email ON account_management.accounts(email);
    CREATE INDEX IF NOT EXISTS idx_accounts_api_key ON account_management.accounts(api_key);
EOF
    
    # Set up users and permissions
    cat << EOF | docker exec -i postgres psql -U ${POSTGRES_USER}
    -- Create application users
    DO \$\$
    BEGIN
        IF NOT EXISTS (SELECT FROM pg_user WHERE usename = 'app_user') THEN
            CREATE USER app_user WITH PASSWORD '${APP_DB_PASSWORD}';
        END IF;
        IF NOT EXISTS (SELECT FROM pg_user WHERE usename = 'read_user') THEN
            CREATE USER read_user WITH PASSWORD '${READ_DB_PASSWORD}';
        END IF;
    END
    \$\$;
    
    -- Grant permissions for task management
    \c taskdb
    GRANT USAGE ON SCHEMA task_management TO app_user;
    GRANT SELECT, INSERT, UPDATE ON ALL TABLES IN SCHEMA task_management TO app_user;
    GRANT USAGE ON ALL SEQUENCES IN SCHEMA task_management TO app_user;
    
    -- Grant permissions for result storage
    \c resultdb
    GRANT USAGE ON SCHEMA result_storage TO app_user;
    GRANT SELECT, INSERT ON ALL TABLES IN SCHEMA result_storage TO app_user;
    GRANT USAGE ON ALL SEQUENCES IN SCHEMA result_storage TO app_user;
    
    -- Grant read-only permissions
    GRANT USAGE ON SCHEMA task_management TO read_user;
    GRANT SELECT ON ALL TABLES IN SCHEMA task_management TO read_user;
    GRANT USAGE ON SCHEMA result_storage TO read_user;
    GRANT SELECT ON ALL TABLES IN SCHEMA result_storage TO read_user;
EOF
    
    log "${GREEN}PostgreSQL initialization completed successfully${NC}"
}

# Redis initialization
init_redis() {
    log "${GREEN}Initializing Redis...${NC}"
    
    # Wait for Redis to be ready
    until docker exec redis redis-cli ping; do
        log "Waiting for Redis to be ready..."
        sleep 2
    done
    
    # Configure Redis
    docker exec redis redis-cli CONFIG SET maxmemory "8gb"
    docker exec redis redis-cli CONFIG SET maxmemory-policy "allkeys-lru"
    docker exec redis redis-cli CONFIG SET appendonly "yes"
    
    # Set up key spaces
    docker exec redis redis-cli SELECT 0  # Default DB for cache
    docker exec redis redis-cli SELECT 1  # Session storage
    docker exec redis redis-cli SELECT 2  # Rate limiting
    
    log "${GREEN}Redis initialization completed successfully${NC}"
}

# Create admin user
create_admin_user() {
    log "${GREEN}Creating admin user...${NC}"
    
    cat << EOF | docker exec -i postgres psql -U ${POSTGRES_USER} -d accountdb
    INSERT INTO account_management.accounts (
        username,
        email,
        password_hash,
        rate_limit
    ) VALUES (
        'admin',
        '${ADMIN_EMAIL}',
        crypt('${ADMIN_PASSWORD}', gen_salt('bf')),
        100000
    ) ON CONFLICT (username) DO NOTHING;
EOF
    
    log "${GREEN}Admin user created successfully${NC}"
}

# Verify installation
verify_installation() {
    log "${GREEN}Verifying database installation...${NC}"
    
    # Check PostgreSQL
    docker exec postgres psql -U ${POSTGRES_USER} -c "\l" || error_handler
    
    # Check Redis
    docker exec redis redis-cli PING || error_handler
    
    log "${GREEN}Database verification completed successfully${NC}"
}

# Main execution
main() {
    log "${GREEN}Starting database initialization process...${NC}"
    
    init_postgresql
    init_redis
    create_admin_user
    verify_installation
    
    log "${GREEN}Database initialization completed successfully!${NC}"
    
    # Generate initialization report
    cat << EOF > ./init_report.txt
Database Initialization Report
============================
Date: $(date)
Status: Success

Initialized Databases:
- PostgreSQL:
  - keycloak
  - kong
  - taskdb
  - resultdb
  - accountdb
- Redis:
  - DB 0: Cache
  - DB 1: Sessions
  - DB 2: Rate Limiting

Created Users:
- app_user (application access)
- read_user (monitoring access)
- admin (system administration)

All schemas and permissions have been configured according to security requirements.
EOF
}

# Execute main function
main