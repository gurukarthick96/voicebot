#!/bin/bash
set -e

echo "Starting uvicorn server on port $APP_PORT..."
exec python -m uvicorn "$APP_PATH" --host "$APP_HOST" --port "$APP_PORT"
