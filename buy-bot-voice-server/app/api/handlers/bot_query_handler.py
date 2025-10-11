from app.ai.audio.decoder import AudioDecoder
from app.ai.audio.decoder.impl import audio_decoder
from app.ai.stt.services import STTService
from app.ai.stt.services.impl import stt_service
from app.ai.tts.services import TTSService
from app.ai.tts.services.impl import tts_service
from app.api.models import BotQueryRequest, BotQueryResponse
from app.bot.client import BotClient
from app.bot.client.impl import bot_client
from app.bot.models import BotMessageApiRequest, BotMessageApiResponse
from app.utils import singleton, logger


@singleton
class BotQueryHandler:

    def __init__(
            self,
            audio_decoder: AudioDecoder,
            stt_service: STTService,
            tts_service: TTSService,
            bot_client: BotClient,
    ):
        self.audio_decoder = audio_decoder
        self.stt_service = stt_service
        self.tts_service = tts_service
        self.bot_client = bot_client

    def handle_query(self, request: BotQueryRequest) -> BotQueryResponse:
        if not request.user_audio and not request.user_text:
            raise ValueError('either user_audio or user_text required')

        user_input = (
            self._transcribe_audio(request.user_audio)
            if request.user_audio else request.user_text
        )

        logger.info('(ID: %s) [USER]: %s', request.session_id, user_input)

        response = self._query_bot(request.session_id, user_input)

        bot_text = ' '.join(response.messages)
        flow_active = bool(response.data.get('ondemand_current_flow'))

        logger.info('(ID: %s) [ BOT]: %s', request.session_id, bot_text)

        audio = (
            self._synthesize([bot_text])
            if request.do_synthesis else None
        )

        return BotQueryResponse(
            user_text=user_input,
            bot_text=bot_text,
            bot_audio=audio,
            flow_active=flow_active
        )

    def _transcribe_audio(self, encoded_audio: str) -> str:
        audio_bytes = self.audio_decoder.decode(encoded_audio)

        return self.stt_service.transcribe_bytes(audio_bytes)

    def _query_bot(self, sender: str, message: str) -> BotMessageApiResponse:
        request = BotMessageApiRequest(sender=sender, message=message)

        response = self.bot_client.send_message(request)

        if not response or not response.messages:
            raise RuntimeError('bot response is empty')

        return response

    def _synthesize(self, texts: list[str]) -> str:
        return self.tts_service.synthesize(texts)


bot_query_handler = BotQueryHandler(audio_decoder, stt_service, tts_service, bot_client)

__all__ = ['BotQueryHandler', 'bot_query_handler']
