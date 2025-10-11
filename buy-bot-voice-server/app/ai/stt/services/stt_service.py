from abc import ABC, abstractmethod

import speech_recognition as sr

from app.utils import normalize_text, bytes_buffer, logger


class STTService(ABC):

    def __init__(self, model_name: str = None, lang: str = None):
        logger.info('initializing %s...', self.__class__.__name__)

        self.model_name = model_name
        self.lang = lang

    def __post_init__(self):
        self.recognizer = sr.Recognizer()

    def transcribe(self, audio: sr.AudioData) -> str:
        if not audio:
            raise RuntimeError('audio is empty')

        try:
            return self._recognize_or_raise(audio)
        except:
            logger.error('unable to transcribe', exc_info=True)
            raise

    def transcribe_bytes(self, audio_bytes: bytes) -> str:
        if not audio_bytes:
            raise RuntimeError('audio bytes is empty')

        with bytes_buffer(audio_bytes) as audio_buffer:
            with sr.AudioFile(audio_buffer) as source:
                audio = self.recognizer.record(source)
                return self.transcribe(audio)

    def _recognize_or_raise(self, audio: sr.AudioData) -> str:
        try:
            text = self._recognize(audio)
            return normalize_text(text)
        except sr.UnknownValueError as e:
            raise RuntimeError(f'could not understand audio: {str(e)}')
        except sr.RequestError as e:
            raise RuntimeError(f'could not recognize audio: {str(e)}')

    @abstractmethod
    def _recognize(self, audio: sr.AudioData) -> str:
        pass
