# VoiceBot

An AI-powered conversational commerce system designed to handle voice and text interactions, process complex actions, and manage bot logic.

## Architecture Overview

The system consists of three main cooperating modules:

1.  **[Voice Server](./buy-bot-voice-server)** (`buy-bot-voice-server`):
    -   Handles Speech-to-Text (STT) and Text-to-Speech (TTS).
    -   Provides a web-based user interface.
    -   Acts as the primary entry point for voice interactions.

2.  **[Bot Server](./buy-bot-server)** (`buy-bot-server`):
    -   The core conversational brain built with Rasa.
    -   Manages dialogue flow and intent recognition.
    -   Communicates with the Action Server for dynamic responses.

3.  **[Action Server](./buy-bot-action-server)** (`buy-bot-action-server`):
    -   Executes custom actions and business logic.
    -   Integrates with LLMs (Google Gemini) and Vector DBs (Qdrant) for RAG capabilities.

## Modules

| Module | Description | Tech Stack |
| :--- | :--- | :--- |
| **[buy-bot-voice-server](./buy-bot-voice-server)** | Voice Interface & UI | FastAPI, Jinja2, STT/TTS |
| **[buy-bot-server](./buy-bot-server)** | Conversational Core | Rasa Pro, Python |
| **[buy-bot-action-server](./buy-bot-action-server)** | Actions & Logic | Rasa SDK, LangChain, Gemini |

## Getting Started

### Prerequisites

-   **Python 3.11+**
-   **[uv](https://docs.astral.sh/uv/)**: Fast Python package manager.
-   **Docker**: For containerized deployment.

### Quick Start

Each module has its own detailed setup instructions. It is recommended to start them in the following order:

1.  **Action Server**: Needs to be running for the Bot Server to execute actions.
    -   [Setup Instructions](./buy-bot-action-server/README.md#local-development)
2.  **Bot Server**: Connects to the Action Server.
    -   [Setup Instructions](./buy-bot-server/README.md#local-development)
3.  **Voice Server**: Connects to the Bot Server.
    -   [Setup Instructions](./buy-bot-voice-server/README.md#local-development)

## Deployment

The system supports deployment via Docker and Azure Kubernetes Service (AKS).

-   **Docker**: Use `poe dbr` (Docker Build Run) in each module to test containerized builds locally.
-   **AKS**: Use `poe deploy` in each module to deploy to a configured Kubernetes cluster.

For detailed deployment steps, please refer to the `README.md` within each module.
