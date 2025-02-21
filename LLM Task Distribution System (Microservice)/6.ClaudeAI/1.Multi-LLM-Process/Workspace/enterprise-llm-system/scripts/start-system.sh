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

# Build and start services
echo "Starting services..."
docker-compose --env-file configs/env/.env up --build -d

# Wait for services to be ready
echo "Waiting for services to start..."
sleep 30

# Initialize Keycloak
echo "Initializing Keycloak..."
./scripts/init-keycloak.sh

# Reload Kong configuration
# echo "Reloading Kong configuration..."
# docker-compose exec api-gateway kong reload

echo "System startup completed!"
