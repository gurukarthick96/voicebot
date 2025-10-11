# ---------- STAGE 1: BASE SYSTEM SETUP ----------
FROM rasa/rasa-pro:3.12.21 AS base-system

# Set common environment variables
ENV WORK_DIR=/opt/agilysys

ENV RASA_PRO_BETA_PREDICATES_IN_RESPONSE_CONDITIONS=true
ENV LLM_API_HEALTH_CHECK=true

WORKDIR $WORK_DIR

# ---------- STAGE 2: MODEL TRAINING ----------
FROM base-system AS model-builder

# Pass docker build arguments (required for model training)
ARG RASA_PRO_LICENSE
ARG GEMINI_API_KEY
ARG RASA_ACTION_ENDPOINT

# Copy full app source (including rasa configuration)
COPY --chown=rasa:rasa app ./app

# Train the model
RUN rasa train \
    --data ./app/rasa/data \
    --config ./app/rasa/config.yml \
    --domain ./app/rasa/domains \
    --endpoints ./app/rasa/endpoints.yml \
    --out ./models \
    --fixed-model-name model \
    -vv

# ---------- STAGE 3: PRODUCTION RUNTIME ----------
FROM base-system AS runtime

# Set runtime-specific environment variables
ENV APP_PORT=5005

# Copy only the trained model and necessary config from builder stage
COPY --from=model-builder --chown=rasa:rasa $WORK_DIR/models ./models
COPY --from=model-builder --chown=rasa:rasa $WORK_DIR/app/rasa/endpoints.yml ./app/rasa/endpoints.yml
COPY --from=model-builder --chown=rasa:rasa $WORK_DIR/app/rasa/credentials.yml ./app/rasa/credentials.yml
COPY --from=model-builder --chown=rasa:rasa $WORK_DIR/app/rasa/channels ./app/rasa/channels

# Copy docker-entrypoint script
COPY --chown=rasa:rasa docker-entrypoint.sh ./docker-entrypoint.sh
RUN chmod +x ./docker-entrypoint.sh

# Expose port
EXPOSE $APP_PORT

# Add health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:$APP_PORT/status || exit 1

# Run the docker-entrypoint script
ENTRYPOINT ["./docker-entrypoint.sh"]
