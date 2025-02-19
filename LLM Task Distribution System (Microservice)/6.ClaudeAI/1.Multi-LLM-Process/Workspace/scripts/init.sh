#!/bin/bash

# # Environment variables
# set -a
# source .env
# set +a

# # Create necessary directories
# mkdir -p {configs,k8s,scripts}
# mkdir -p configs/{nginx,keycloak,kafka,redis,postgresql,prometheus}/ssl

# # Copy configuration files
# echo "Copying configuration files..."
# cp nginx.conf configs/nginx/
# cp prometheus.yml configs/prometheus/
# cp server.properties configs/kafka/
# cp postgresql.conf configs/postgresql/
# cp redis.conf configs/redis/

# Set proper permissions
chmod 600 configs/postgresql/postgresql.conf
chmod 600 configs/redis/redis.conf
chmod -R 644 configs/prometheus
chmod -R 644 configs/nginx

# Initialize Docker networks
echo "Creating Docker networks..."
docker network create frontend
docker network create security
docker network create processing
docker network create orchestration
docker network create queue
docker network create database
docker network create cache
docker network create monitoring
docker network create storage

# Start core services
echo "Starting core services..."
docker-compose up -d postgres redis kafka zookeeper

# Wait for core services
echo "Waiting for core services to be ready..."
sleep 30

# Start remaining services
echo "Starting remaining services..."
docker-compose up -d

# Health check
echo "Performing health check..."
./scripts/health-check.sh

echo "Deployment complete. Please check docker-compose ps for service status."