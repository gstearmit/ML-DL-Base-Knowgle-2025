#!/bin/bash

# Wait for Keycloak to start
echo "Waiting for Keycloak to start..."
max_attempts=30
attempt=1

while ! curl -s http://localhost:8180/health > /dev/null; do
    if [ $attempt -gt $max_attempts ]; then
        echo "Keycloak failed to start after $max_attempts attempts"
        exit 1
    fi
    echo "Attempt $attempt: Keycloak not ready, waiting..."
    sleep 10
    attempt=$((attempt + 1))
done

echo "Keycloak is running"

# Get admin token
echo "Getting admin token..."
TOKEN_RESPONSE=$(curl -s -X POST http://localhost:8180/realms/master/protocol/openid-connect/token \
    -H 'Content-Type: application/x-www-form-urlencoded' \
    --data-urlencode "client_id=admin-cli" \
    --data-urlencode "username=admin" \
    --data-urlencode "password=admin" \
    --data-urlencode "grant_type=password")

if [ -z "$TOKEN_RESPONSE" ]; then
    echo "Failed to get token response"
    exit 1
fi

ADMIN_TOKEN=$(echo $TOKEN_RESPONSE | jq -r '.access_token')

if [ -z "$ADMIN_TOKEN" ] || [ "$ADMIN_TOKEN" = "null" ]; then
    echo "Failed to extract token from response:"
    echo $TOKEN_RESPONSE
    exit 1
fi

echo "Admin token obtained successfully"

# Create realm
echo "Creating realm..."
REALM_RESPONSE=$(curl -s -X POST http://localhost:8180/admin/realms \
    -H "Authorization: Bearer $ADMIN_TOKEN" \
    -H "Content-Type: application/json" \
    -d @configs/keycloak/realm-config.json)

if [ ! -z "$REALM_RESPONSE" ]; then
    echo "Realm creation response:"
    echo $REALM_RESPONSE
fi

# Verify realm creation
echo "Verifying realm creation..."
VERIFY_RESPONSE=$(curl -s -X GET http://localhost:8180/admin/realms/llm-system \
    -H "Authorization: Bearer $ADMIN_TOKEN")

if [ -z "$VERIFY_RESPONSE" ]; then
    echo "Failed to verify realm creation"
    exit 1
fi

# Verify client creation
echo "Verifying client configuration..."
CLIENT_RESPONSE=$(curl -s -X GET http://localhost:8180/admin/realms/llm-system/clients \
    -H "Authorization: Bearer $ADMIN_TOKEN" \
    -H "Content-Type: application/json")

if [ -z "$CLIENT_RESPONSE" ]; then
    echo "Failed to verify client configuration"
    exit 1
fi

echo "Keycloak setup completed successfully!" 