#!/bin/bash

set -e

function create_database() {
    local database=$1
    local app_user=$2
    local app_password=$3
    echo "Checking and creating database '$database' and user '$app_user' if not exists"
    
    # Connect to default postgres database first
    psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "postgres" <<-EOSQL
        -- Create user if not exists
        DO \$\$
        BEGIN
            IF NOT EXISTS (SELECT FROM pg_catalog.pg_roles WHERE rolname = '$app_user') THEN
                CREATE USER $app_user WITH PASSWORD '$app_password';
            END IF;
        END
        \$\$;

        -- Create database if not exists
        SELECT 'CREATE DATABASE $database'
        WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = '$database')\gexec

        -- Grant privileges
        GRANT ALL PRIVILEGES ON DATABASE $database TO $app_user;
EOSQL

    # Connect to the new database to set schema permissions
    psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$database" <<-EOSQL
        GRANT ALL ON SCHEMA public TO $app_user;
EOSQL
}

# Split the comma-separated lists into arrays
IFS=',' read -r -a dbs <<< "$POSTGRES_ADDITIONAL_DBS"
IFS=',' read -r -a users <<< "$POSTGRES_ADDITIONAL_USERS"
IFS=',' read -r -a passwords <<< "$POSTGRES_ADDITIONAL_PASSWORDS"

# Create each database and user pair
for i in "${!dbs[@]}"; do
    if [ -n "${dbs[$i]}" ] && [ -n "${users[$i]}" ] && [ -n "${passwords[$i]}" ]; then
        create_database "${dbs[$i]}" "${users[$i]}" "${passwords[$i]}"
    fi
done

echo "Database initialization completed"
