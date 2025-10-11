#!/bin/bash
set -e

# Set default values
RUN_MODE=${RUN_MODE:-server}
DEBUG=${DEBUG:-false}

# Set verbosity based on DEBUG flag
if [ "$DEBUG" = "true" ] || [ "$DEBUG" = "1" ]; then
    VERBOSE_FLAG="-vv"
    echo "Debug mode enabled - verbose logging active"
else
    VERBOSE_FLAG=""
    echo "Debug mode disabled - normal logging"
fi

case "$RUN_MODE" in
    "server")
        echo "Starting Rasa server on port $APP_PORT..."
        exec python -m rasa run --enable-api --cors "*" --port $APP_PORT --endpoints ./app/rasa/endpoints.yml --credentials ./app/rasa/credentials.yml $VERBOSE_FLAG
        ;;
    "inspect")
        echo "Starting Rasa inspect on port $APP_PORT..."
        exec python -m rasa inspect --port $APP_PORT --endpoints ./app/rasa/endpoints.yml $VERBOSE_FLAG
        ;;
    *)
        echo "Defaulting to server mode. Starting Rasa server on port $APP_PORT..."
        exec python -m rasa run --enable-api --cors "*" --port $APP_PORT --endpoints ./app/rasa/endpoints.yml --credentials ./app/rasa/credentials.yml $VERBOSE_FLAG
        ;;
esac
