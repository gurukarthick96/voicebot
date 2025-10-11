# Buy Bot Action Server

An AI-powered bot action server built with Rasa SDK, integrated with LLM and Vector DB.

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
- **docker run -p 6333:6333 --name qdrant-db -d qdrant/qdrant** - Run Qdrant VectorDB locally if needed
- **Administrator privileges** (required for some operations)

## Local Development

### 1. Installation

```bash
cd buy-bot-action-server
uv sync --dev -U
```

> **Note**: This automatically installs `poe`, a task runner for shorthand commands.

### 2. Environment Configuration

#### System Environment Variables

Set the following environment variables:

| Variable         | Description           | Source                                                 |
|------------------|-----------------------|--------------------------------------------------------|
| `GEMINI_API_KEY` | Google Gemini API key | [Google AI Studio](https://aistudio.google.com/apikey) |
| `ENVIRONMENT`    | Set to `local`        | -                                                      |

#### .env File Configuration

Replace below envs from `.env` file with:

```env
LOGGING_LEVEL=INFO
VECTOR_DB_URL=<IN_MEMORY> or <HOSTED_VECTOR_DB_URL>
GEMINI_MODEL_NAME=<GEMINI_MODEL_FOR_LLM>
TEXT_EMBEDDING_MODEL_NAME=<TRANSFORMER_MODEL_FOR_TEXT_EMBEDDING>
```

> **Note**: Only modify other values if you need a custom setup.

### 3. Running the Action Server

#### Launch the Action Server

```bash
poe a  # or poe actions
```

> **Important**: Run commands as administrator.

### 4. Health Check

Test the server with:

```bash
GET /health
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
GET /health
```

Returns the server status.

## Troubleshooting

### Common Issues

1. **Permission Errors**: Ensure you're running commands as administrator
2. **Environment Variables**: Verify all required environment variables are set
3. **API Key Issues**: Ensure your Gemini API key is active and has sufficient quotas

### Getting Help

- Review logs using `poe` commands with verbose flags
- Ensure all prerequisites are properly installed

## Available Commands

| Command        | Description                 |
|----------------|-----------------------------|
| `poe a`        | Start Action server         |
| `poe dbr`      | Docker build and run        |
| `poe dbtp`     | Docker build, tag, and push |
| `poe deploy`   | Deploy to AKS               |
| `poe undeploy` | Remove from AKS             |

---

For more detailed information about specific commands, run `poe --help`.
