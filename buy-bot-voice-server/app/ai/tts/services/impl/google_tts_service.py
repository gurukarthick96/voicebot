from gtts import gTTS
from typing_extensions import override

from app.ai.audio.encoder.impl import audio_encoder
from app.ai.tts.services import TTSService
from app.utils import singleton, post_init, bytes_buffer


@singleton
@post_init
class GoogleTTSService(TTSService):

    @override
    def __init__(self, lang: str = 'en'):
        super().__init__()

        self.lang = lang

    @override
    def __post_init__(self):
        super().__post_init__()

    @override
    def speak(self, texts: list[str]) -> None:
        raise NotImplementedError()

    @override
    def synthesize(self, texts: list[str]) -> str:
        tts = gTTS(text=' '.join(texts), lang=self.lang)

        with bytes_buffer() as audio_buffer:
            tts.write_to_fp(audio_buffer)
            return audio_encoder.encode(audio_buffer.getvalue())


google_tts_service = GoogleTTSService()

__all__ = ['google_tts_service']
