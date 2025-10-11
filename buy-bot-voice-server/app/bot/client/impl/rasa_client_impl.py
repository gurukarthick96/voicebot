from functools import cached_property
from typing import Any

from typing_extensions import override

from app import config
from app.bot.client import BotClient
from app.bot.models import BotMessageApiRequest, BotMessageApiResponse


class RasaClientImpl(BotClient):
    @cached_property
    def health_check_url(self) -> str:
        return f'{self.base_url}/status'

    @cached_property
    def webhook_url(self) -> str:
        return f'{self.base_url}/webhooks/{self.channel_name}/webhook'

    @cached_property
    def conversation_url_template(self) -> str:
        return f'{self.base_url}/conversations/{{sender}}/execute'

    @cached_property
    def headers(self) -> dict[str, str]:
        return {'Authorization': f'Bearer {self.api_key}'} if self.api_key else {}

    @override
    def health_check(self) -> None:
        self._get(self.health_check_url)

    @override
    def restart_conversation(self, sender: str) -> None:
        url = self.conversation_url_template.format(sender=sender)

        payload = {'name': 'action_restart'}

        self._post(url, payload)

    @override
    def send_message(self, request: BotMessageApiRequest) -> BotMessageApiResponse:
        response_data = self._post(self.webhook_url, request.model_dump())

        return self._validate_and_parse_response(request.sender, response_data)

    @staticmethod
    def _validate_and_parse_response(sender: str, data: dict[str, Any]) -> BotMessageApiResponse:
        bot_message_response = BotMessageApiResponse(**data)

        if sender != bot_message_response.conversation_id:
            raise RuntimeError('sender id does not match conversation id')

        return bot_message_response


rasa_client = RasaClientImpl(config.BOT_CLIENT_BASE_URL, config.BOT_CLIENT_CHANNEL_NAME)

__all__ = ['rasa_client']
