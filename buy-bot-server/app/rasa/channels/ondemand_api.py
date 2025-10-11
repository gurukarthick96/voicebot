from typing import Text, Callable, Awaitable, Any, Optional

from rasa.core.channels.channel import UserMessage, InputChannel, CollectingOutputChannel
from sanic import Blueprint, response
from sanic.request import Request
from sanic.response import HTTPResponse


class OnDemandAPIChannel(InputChannel):
    def name(self) -> Text:
        return 'ondemand_api'

    def blueprint(
            self, on_new_message: Callable[[UserMessage], Awaitable[None]]
    ) -> Blueprint:
        webhook = Blueprint('ondemand_api_webhook', __name__)

        @webhook.route('/', methods=['GET'])
        async def health(request: Request) -> HTTPResponse:
            return response.json({'status': 'ok'})

        @webhook.route('/webhook', methods=['POST'])
        async def receive(request: Request) -> HTTPResponse:
            return await self.receive_http_response(request, on_new_message)

        return webhook

    async def receive_http_response(
            self, request: Request, on_new_message: Callable[[UserMessage], Awaitable[None]]
    ) -> HTTPResponse:
        try:
            payload = request.json

            sender_id = payload.get('sender')
            text = payload.get('message')

            if not sender_id or not text:
                return response.json({'error': 'Missing sender or message'}, status=400)

            result = await self._handle_message(sender_id, text, on_new_message)

            return response.json(result)

        except Exception as e:
            return response.json({'error': str(e)}, status=500)

    async def _handle_message(
            self, sender_id: str, text: str, on_new_message: Callable[[UserMessage], Awaitable[None]]
    ) -> dict[str, Any]:
        collector = CollectingOutputChannel()

        await on_new_message(
            UserMessage(
                text,
                collector,
                sender_id,
            )
        )

        return self._build_response(collector, sender_id)

    def _build_response(self, collector: CollectingOutputChannel, sender_id: str) -> dict[str, Any]:
        return {
            'conversation_id': sender_id,
            'messages': self._filter_messages_by_sender(collector.messages, sender_id),
            'data': self._build_data_from_tracker(collector.tracker_state),
        }

    @staticmethod
    def _filter_messages_by_sender(messages: list[dict[str, Any]], sender_id: str) -> list[str]:
        return [
            text
            for msg in messages
            if (text := msg.get('text')) and msg.get('recipient_id') == sender_id
        ]

    @staticmethod
    def _build_data_from_tracker(tracker_state: Optional[dict[str, Any]]) -> dict[str, Any]:
        data = {}

        if tracker_state and (slots := tracker_state.get('slots')):
            data['order'] = slots.get('order')
            data['ondemand_current_flow'] = slots.get('ondemand_current_flow')

        return data
