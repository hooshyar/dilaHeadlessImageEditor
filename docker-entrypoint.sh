#!/bin/bash
set -e

# Create necessary directories if they don't exist
mkdir -p /app/output/images
mkdir -p /app/output/temp
mkdir -p /app/app/templates
mkdir -p /app/fonts

# Copy templates if they don't exist
if [ ! -f /app/app/templates/index.html ]; then
    echo "Copying index.html template"
    cp -n /app/templates/index.html /app/app/templates/ 2>/dev/null || true
fi

if [ ! -f /app/app/templates/playground.html ]; then
    echo "Copying playground.html template"
    cp -n /app/templates/playground.html /app/app/templates/ 2>/dev/null || true
fi

# Run the application
if [ "$1" = "dev" ]; then
    echo "Running in development mode"
    exec python -m run --port $PORT --debug
else
    echo "Running in production mode"
    exec gunicorn --bind 0.0.0.0:$PORT --workers 4 "run:create_app()"
fi 