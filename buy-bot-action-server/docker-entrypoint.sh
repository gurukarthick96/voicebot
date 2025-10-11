#!/bin/bash
set -e

# Set default values
DEBUG=${DEBUG:-false}

# Set verbosity based on DEBUG flag
if [ "$DEBUG" = "true" ] || [ "$DEBUG" = "1" ]; then
    VERBOSE_FLAG="-vv"
    echo "Debug mode enabled - verbose logging active"
else
    VERBOSE_FLAG=""
    echo "Debug mode disabled - normal logging"
fi

echo "Starting Rasa action server on port $APP_PORT..."
exec python -m rasa_sdk --port 5055 --actions app.rasa.actions --endpoints app/rasa/endpoints.yml $VERBOSE_FLAG
