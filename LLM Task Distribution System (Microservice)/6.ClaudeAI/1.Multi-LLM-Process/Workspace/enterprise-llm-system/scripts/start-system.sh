#!/bin/bash

# Make scripts executable
chmod +x scripts/*.sh

# Check if running with sudo
if [ "$EUID" -ne 0 ]; then 
    echo "Please run with sudo to ensure proper permissions"
    exit 1
fi

# Check environment variables
./scripts/check-env.sh
if [ $? -ne 0 ]; then
    echo "Please fix environment variables and try again."
    exit 1
fi

# Check if script has execute permission
if [ ! -x "scripts/init-multiple-postgres-databases.sh" ]; then
    echo "Setting execute permission for init-multiple-postgres-databases.sh"
    chmod +x scripts/init-multiple-postgres-databases.sh
fi

# Stop and remove existing containers
echo "Stopping existing containers..."
docker-compose down -v

# Remove existing volumes
echo "Cleaning up volumes..."
docker volume prune -f
docker volume rm enterprise-llm-system_postgres_data

# Build and start services
echo "Starting services..."
docker-compose --env-file configs/env/.env up --build -d

# docker builder prune
# docker-compose --env-file configs/env/.env up --build 
# docker-compose --env-file configs/env/.env up -d api-gateway
# docker-compose exec api-gateway kong reload


# Wait for services to be ready
echo "Waiting for services to start..."
sleep 30

# Initialize Keycloak
echo "Initializing Keycloak..."
chmod +x ./scripts/init-keycloak.sh
./scripts/init-keycloak.sh

# Wait for services to be ready
echo "Waiting for services to start..."
sleep 30

# Initialize multiple PostgreSQL databases
echo "Initializing multiple PostgreSQL databases..."
chmod +x ./scripts/init-multiple-postgres-databases.sh
./scripts/init-multiple-postgres-databases.sh
 
# Wait for services to be ready
echo "Waiting for services to start..."
sleep 10

echo "System startup completed!"
