# Buy Bot Server

An AI-powered conversational bot server built with [Rasa](https://rasa.com/), a leading conversational AI framework.

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
cd buy-bot-server
uv sync --dev -U
```

> **Note**: This automatically installs `poe`, a task runner for shorthand commands.

### 2. Environment Configuration

#### System Environment Variables

Set the following environment variables:

| Variable           | Description           | Source                                                                                   |
|--------------------|-----------------------|------------------------------------------------------------------------------------------|
| `RASA_PRO_LICENSE` | Rasa Pro license key  | [Rasa Pro License Page](https://rasa.com/rasa-pro-developer-edition-license-key-request) |
| `GEMINI_API_KEY`   | Google Gemini API key | [Google AI Studio](https://aistudio.google.com/apikey)                                   |
| `ENVIRONMENT`      | Set to `local`        | -                                                                                        |

#### .env File Configuration

Replace below envs from `.env` file with:

```env
RASA_ACTION_ENDPOINT=<bot-action-server-webhook-endpoint>
```

> **Note**: Only modify other values if you need a custom setup.

### 3. Running the Server

#### Train and Launch API Server

```bash
poe cta  # or poe clean-train-api
```

#### Run in Inspect Mode

```bash
poe cti  # or poe clean-train-inspect
```

> **Important**: Run commands as administrator.

### 4. Health Check

Test the server with:

```bash
GET /status
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

### 2. Secrets Setup (One-time per environment)

```bash
bash azure-pipelines/apply-secret.sh
```

This adds the following secrets to AKS:

- `RASA_PRO_LICENSE`
- `GEMINI_API_KEY`

### 3. Deployment Commands

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
GET /status
```

Returns the server status and health information.

## Troubleshooting

### Common Issues

1. **Permission Errors**: Ensure you're running commands as administrator
2. **Environment Variables**: Verify all required environment variables are set
3. **License Issues**: Check that your Rasa Pro license is valid and properly configured
4. **API Key Issues**: Ensure your Gemini API key is active and has sufficient quotas

### Getting Help

- Check the [Rasa Documentation](https://rasa.com/docs/)
- Review logs using `poe` commands with verbose flags
- Ensure all prerequisites are properly installed

## Available Commands

| Command        | Description                             |
|----------------|-----------------------------------------|
| `poe cta`      | Clean, train, and start API server      |
| `poe cti`      | Clean, train, and start in inspect mode |
| `poe dbr`      | Docker build and run                    |
| `poe dbtp`     | Docker build, tag, and push             |
| `poe deploy`   | Deploy to AKS                           |
| `poe undeploy` | Remove from AKS                         |

---

For more detailed information about specific commands, run `poe --help`.
