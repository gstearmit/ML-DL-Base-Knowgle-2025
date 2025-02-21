#!/bin/bash

ENV_FILE="configs/env/.env"
ENV_EXAMPLE_FILE="configs/env/.env.example"

# Check if .env file exists
if [ ! -f "$ENV_FILE" ]; then
    echo "Warning: .env file not found"
    echo "Creating .env file from .env.example..."
    cp "$ENV_EXAMPLE_FILE" "$ENV_FILE"
    echo ".env file created. Please review and update the values."
    exit 1
fi

# Read required variables from .env.example
required_vars=$(grep -v '^#' "$ENV_EXAMPLE_FILE" | cut -d '=' -f1)

# Check each required variable
missing_vars=()
for var in $required_vars; do
    if ! grep -q "^${var}=" "$ENV_FILE"; then
        missing_vars+=("$var")
    fi
done

# If any variables are missing, show error and exit
if [ ${#missing_vars[@]} -ne 0 ]; then
    echo "Error: Missing required environment variables:"
    printf '%s\n' "${missing_vars[@]}"
    echo "Please update your .env file with the missing variables."
    exit 1
fi

echo "Environment validation successful!" 