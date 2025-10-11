import speech_recognition as sr
import vosk
from typing_extensions import override

from app.ai.stt.services import STTService
from app.utils import json_to_dict, singleton, post_init


@singleton
@post_init
class VoskSTTService(STTService):

    @override
    def __post_init__(self):
        super().__post_init__()

        self.recognizer.vosk_model = vosk.Model(model_name=self.model_name, lang=self.lang)

    @override
    def _recognize(self, audio: sr.AudioData) -> str:
        json_text = self.recognizer.recognize_vosk(audio)

        return self._parse_text(json_text)

    @staticmethod
    def _parse_text(json_text) -> str:
        return json_to_dict(json_text).get('text')


vosk_stt_service = VoskSTTService('vosk-model-small-en-us-0.15')

__all__ = ['vosk_stt_service']
