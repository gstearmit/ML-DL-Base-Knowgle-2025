#!/bin/bash

set -e

function create_database() {
    local database=$1
    echo "Creating database '$database'"
    psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" <<-EOSQL
        CREATE DATABASE $database;
        GRANT ALL PRIVILEGES ON DATABASE $database TO $POSTGRES_USER;
EOSQL
}

# Check if POSTGRES_MULTIPLE_DATABASES is set
if [ -z "${POSTGRES_MULTIPLE_DATABASES:-}" ]; then
    echo "POSTGRES_MULTIPLE_DATABASES is not set, skipping additional database creation"
    exit 0
fi

echo "Multiple database creation requested: $POSTGRES_MULTIPLE_DATABASES"
for db in $(echo $POSTGRES_MULTIPLE_DATABASES | tr ',' ' '); do
    create_database $db
done
echo "Multiple databases created" 