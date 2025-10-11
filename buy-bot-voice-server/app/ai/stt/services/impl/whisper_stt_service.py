import speech_recognition as sr
from typing_extensions import override

from app.ai.stt.services import STTService
from app.utils import singleton, post_init


@singleton
@post_init
class WhisperSTTService(STTService):

    @override
    def __post_init__(self):
        super().__post_init__()

    @override
    def _recognize(self, audio: sr.AudioData) -> str:
        return self.recognizer.recognize_faster_whisper(audio_data=audio, model=self.model_name)


whisper_stt_service = WhisperSTTService('small.en')

__all__ = ['whisper_stt_service']
