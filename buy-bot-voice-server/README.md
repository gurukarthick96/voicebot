# Buy Bot Voice Server

An AI-powered bot voice server built with FastAPI and integrated with Speech-to-Text (STT) and Text-to-Speech (TTS)
components. It also features a simple static UI with Jinja2.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Local Development](#local-development)
- [Docker Deployment](#docker-deployment)
- [Azure Kubernetes Service (AKS) Deployment](#azure-kubernetes-service-aks-deployment)
- [API Reference](#api-reference)
- [Troubleshooting](#troubleshooting)

## Prerequisites

- **Python 3.11+**
- **[uv](https://docs.astral.sh/uv/getting-started/installation/)** - A fast Python package manager
- **Administrator privileges** (required for some operations)

## Local Development

### 1. Installation

```bash
cd buy-bot-voice-server
uv sync --dev -U
```

> **Note**: This automatically installs `poe`, a task runner for shorthand commands.

### 2. Environment Configuration

#### System Environment Variables

Set the following environment variables:

| Variable      | Description    | Source |
|---------------|----------------|--------|
| `ENVIRONMENT` | Set to `local` | -      |

#### .env File Configuration

Replace below envs from `.env` file with:

```env
LOGGING_LEVEL=INFO
BOT_CLIENT_BASE_URL=<BOT_SERVER_URL>
```

> **Note**: Only modify other values if you need a custom setup.

### 3. Running the Voice API Server

#### Launch the Voice API Server

```bash
poe a  # or poe api
```

> **Important**: Run commands as administrator.

### 4. Health Check

Test the server with:

```bash
GET /internal/health
```

## Docker Deployment

### Development Testing

Build and run locally:

```bash
poe dbr  # or poe docker-build-run
```

### Build and Push to Registry

Push to AQYSACRQA registry:

```bash
poe dbtp  # or poe docker-build-tag-push
```

## Azure Kubernetes Service (AKS) Deployment

### 1. Configuration

Update your configuration file:

```
azure-pipelines/k8s.service.configMap.yaml
```

Ensure all environment values are correctly set.

### 2. Deployment Commands

Deploy to AKS:

```bash
poe deploy
```

Remove from AKS:

```bash
poe undeploy
```

## API Reference

### Health Check

```http
GET /internal/health
```

Returns the API server status and health information.

## Troubleshooting

### Common Issues

1. **Permission Errors**: Ensure you're running commands as administrator
2. **Environment Variables**: Verify all required environment variables are set

### Getting Help

- Review logs using `poe` commands with verbose flags
- Ensure all prerequisites are properly installed

## Available Commands

| Command        | Description                 |
|----------------|-----------------------------|
| `poe a`        | Start Voice API server      |
| `poe dbr`      | Docker build and run        |
| `poe dbtp`     | Docker build, tag, and push |
| `poe deploy`   | Deploy to AKS               |
| `poe undeploy` | Remove from AKS             |

---

For more detailed information about specific commands, run `poe --help`.
