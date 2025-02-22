# Enterprise LLM System

http://localhost:8180/realms/llm-system

http://localhost:8180/realms/llm-system/protocol/openid-connect/certs


Task Manager API: http://localhost:8080/api/tasks
Auth Service API: http://localhost:8080/api/auth
Keycloak Admin Console: http://localhost:8180

Kiểm tra logs để theo dõi quá trình khởi động:
docker compose logs -f
Thứ tự khởi động sẽ là:

PostgreSQL khởi động và khởi tạo databases
Keycloak đợi PostgreSQL healthy và khởi động
Kong API Gateway khởi động
Auth Service và Task Manager đợi các dependency sẵn sàng rồi khởi động
Các cải thiện này sẽ giúp:

Đảm bảo các service khởi động theo đúng thứ tự
Tự động thử lại khi gặp lỗi
Kiểm tra health tốt hơn
Giám sát trạng thái service dễ dàng hơn

## Prerequisites

- Docker and Docker Compose
- sudo privileges

## Setup

1. Clone repository:
```bash
git clone <repository-url>
cd enterprise-llm-system
```

2. Set up environment variables:
```bash
# Copy example environment file
cp configs/env/.env.example configs/env/.env

# Edit environment variables
nano configs/env/.env
```

3. Start the system:
```bash
# Run with sudo to ensure proper permissions
sudo ./scripts/start-system.sh
```

## Environment Variables

Required environment variables are:

### PostgreSQL Configuration
- POSTGRES_USER: PostgreSQL username
- POSTGRES_PASSWORD: PostgreSQL password
- POSTGRES_DB: Main application database name
- POSTGRES_KEYCLOAK_DB: Keycloak database name
- POSTGRES_KEYCLOAK_USER: Keycloak database user
- POSTGRES_KEYCLOAK_PASSWORD: Keycloak database password

### Other Services
- API_GATEWAY_PORT: Port for Kong API Gateway (default: 8080)
- KONG_ADMIN_TOKEN: Admin token for Kong
- KEYCLOAK_ADMIN_USERNAME: Keycloak admin username
- KEYCLOAK_ADMIN_PASSWORD: Keycloak admin password
- TASK_MANAGER_PORT: Port for Task Manager service (default: 8081)
- AUTH_SERVICE_PORT: Port for Auth service (default: 8082)
- REDIS_PORT: Port for Redis (default: 6379)

See configs/env/.env.example for all available variables.

## Troubleshooting

If you encounter permission issues:

1. Check script permissions:
```bash
ls -l scripts/
```

2. Set execute permissions if needed:
```bash
chmod +x scripts/*.sh
```

3. Run with sudo:
```bash
sudo ./scripts/start-system.sh
``` 

```bash
docker-compose --env-file configs/env/.env up --build 

docker-compose --env-file configs/env/.env up -d api-gateway
```

docker-compose exec api-gateway kong reload