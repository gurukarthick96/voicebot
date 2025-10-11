# ---------- STAGE 1: PYTHON VIRTUAL ENVIRONMENT SETUP ----------
FROM ghcr.io/astral-sh/uv:python3.11-bookworm-slim AS pyvenv

# Set environment variables
ENV WORK_DIR=/opt/agilysys

WORKDIR $WORK_DIR

# Copy dependency files
COPY pyproject.toml uv.lock ./

# Setup venv and install python dependencies
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev

# ---------- STAGE 2: BASE SYSTEM SETUP ----------
FROM python:3.11-slim-bookworm AS base-system

# Install ffmpeg, system dependencies and security updates
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        flac \
        ffmpeg \
        curl \
        ca-certificates && \
    apt-get upgrade -y && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Create non-root user for security
RUN groupadd --gid 1001 appuser && \
    useradd --uid 1001 --gid appuser --shell /bin/bash --create-home appuser

# Set system-specific environment variables
ENV WORK_DIR=/opt/agilysys

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONPATH=$WORK_DIR \
    PATH="$WORK_DIR/.venv/bin:$PATH" \
    UV_SYSTEM_PYTHON=1

# Create work directory and set ownership
RUN mkdir -p $WORK_DIR && \
    chown -R appuser:appuser $WORK_DIR

WORKDIR $WORK_DIR

# Copy virtual environment from pyvenv stage
COPY --from=pyvenv --chown=appuser:appuser $WORK_DIR/.venv ./.venv

# ---------- STAGE 3: PRODUCTION RUNTIME ----------
FROM base-system AS runtime

# Set runtime-specific environment variables
ENV APP_PATH=app:voiceapp
ENV APP_HOST=0.0.0.0
ENV APP_PORT=8000

# Copy application code and ui contents
COPY --chown=appuser:appuser app ./app
COPY --chown=appuser:appuser static ./static
COPY --chown=appuser:appuser templates ./templates

# Copy docker-entrypoint script
COPY --chown=appuser:appuser docker-entrypoint.sh ./docker-entrypoint.sh
RUN chmod +x ./docker-entrypoint.sh

# Switch to non-root user
USER appuser

# Expose port
EXPOSE $APP_PORT

# Add health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:$APP_PORT/internal/health || exit 1

# Run the docker-entrypoint script
ENTRYPOINT ["./docker-entrypoint.sh"]
