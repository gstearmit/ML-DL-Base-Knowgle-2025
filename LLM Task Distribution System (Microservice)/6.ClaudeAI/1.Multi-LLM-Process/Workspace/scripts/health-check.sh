#!/bin/bash

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

check_service() {
    local service=$1
    local port=$2
    echo -n "Checking $service... "
    
    if nc -z localhost $port >/dev/null 2>&1; then
        echo -e "${GREEN}OK${NC}"
        return 0
    else
        echo -e "${RED}FAILED${NC}"
        return 1
    fi
}

check_docker_service() {
    local service=$1
    echo -n "Checking Docker service $service... "
    
    if docker-compose ps | grep $service | grep "Up" >/dev/null 2>&1; then
        echo -e "${GREEN}OK${NC}"
        return 0
    else
        echo -e "${RED}FAILED${NC}"
        return 1
    fi
}

# Main health checks
echo "Starting health checks..."

# Core Infrastructure
check_service "Nginx" 80
check_service "Kong" 8000
check_service "Keycloak" 8080
check_service "PostgreSQL" 5432
check_service "Redis" 6379
check_service "RabbitMQ" 5672
check_service "Kafka" 9092
check_service "MinIO" 9000
check_service "Prometheus" 9090
check_service "Grafana" 3000

# Docker Services
echo -e "\nChecking Docker services..."
services=(
    "nginx"
    "kong"
    "keycloak"
    "postgres"
    "redis"
    "rabbitmq"
    "kafka"
    "minio"
    "prometheus"
    "grafana"
    "llm-engine"
)

failed_services=()
for service in "${services[@]}"; do
    if ! check_docker_service $service; then
        failed_services+=($service)
    fi
done

# Summary
echo -e "\nHealth Check Summary:"
if [ ${#failed_services[@]} -eq 0 ]; then
    echo -e "${GREEN}All services are running correctly${NC}"
else
    echo -e "${RED}The following services have issues:${NC}"
    for service in "${failed_services[@]}"; do
        echo -e "${YELLOW}- $service${NC}"
    done
    exit 1
fi