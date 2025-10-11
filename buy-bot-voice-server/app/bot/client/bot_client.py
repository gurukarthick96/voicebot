from abc import ABC, abstractmethod
from typing import Any

import requests

from app.bot.models import BotMessageApiRequest, BotMessageApiResponse


class BotClient(ABC):
    def __init__(self, base_url: str, channel_name: str, api_key: str = None):
        self.base_url = base_url
        self.channel_name = channel_name
        self.api_key = api_key

    @property
    @abstractmethod
    def headers(self) -> dict[str, str]:
        pass

    @abstractmethod
    def health_check(self) -> None:
        pass

    @abstractmethod
    def restart_conversation(self, sender: str) -> None:
        pass

    @abstractmethod
    def send_message(self, request: BotMessageApiRequest) -> BotMessageApiResponse:
        pass

    def _get(self, url: str) -> dict[str, Any]:
        response = requests.get(url, headers=self.headers)

        response.raise_for_status()

        return response.json()

    def _post(self, url: str, payload: dict[str, Any]) -> dict[str, Any]:
        response = requests.post(url, json=payload, headers=self.headers)

        response.raise_for_status()

        return response.json()


__all__ = ['BotClient']
