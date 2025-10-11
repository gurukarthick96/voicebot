import speech_recognition as sr
from typing_extensions import override

from app.ai.stt.services import STTService
from app.utils import singleton, post_init


@singleton
@post_init
class GoogleSTTService(STTService):

    @override
    def __post_init__(self):
        super().__post_init__()

    @override
    def _recognize(self, audio: sr.AudioData) -> str:
        return self.recognizer.recognize_google(audio_data=audio)


google_stt_service = GoogleSTTService()

__all__ = ['google_stt_service']
