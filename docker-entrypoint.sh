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

# Set default timeouts if not provided
: "${REQUEST_TIMEOUT:=60}"
: "${TASK_TIMEOUT:=300}"
: "${SESSION_TIMEOUT:=600}"

# Add timeout monitor that shuts down server after inactivity
(
    sleep $SESSION_TIMEOUT
    echo "Maximum session time of $SESSION_TIMEOUT seconds reached. Shutting down container."
    kill -15 1  # Send SIGTERM to PID 1 (main process)
) &
TIMEOUT_MONITOR_PID=$!

# Function to clean up timeout monitor on exit
cleanup() {
    echo "Cleaning up resources..."
    kill $TIMEOUT_MONITOR_PID 2>/dev/null || true
}

# Register cleanup function
trap cleanup EXIT

# Run the application
if [ "$1" = "dev" ]; then
    echo "Running in development mode with timeouts: REQUEST=$REQUEST_TIMEOUT, TASK=$TASK_TIMEOUT, SESSION=$SESSION_TIMEOUT"
    exec python -m run --port $PORT --debug --request-timeout $REQUEST_TIMEOUT --task-timeout $TASK_TIMEOUT
else
    echo "Running in production mode with timeouts: REQUEST=$REQUEST_TIMEOUT, TASK=$TASK_TIMEOUT, SESSION=$SESSION_TIMEOUT"
    exec gunicorn --bind 0.0.0.0:$PORT --workers 4 --timeout $REQUEST_TIMEOUT "run:create_app()"
fi 