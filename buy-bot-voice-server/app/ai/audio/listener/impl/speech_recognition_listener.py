from functools import cached_property

import speech_recognition as sr
from typing_extensions import override

from app.ai.audio.listener import AudioListener
from app.utils import post_init, singleton, logger


@singleton
@post_init
class SpeechRecognitionListener(AudioListener):

    @override
    def __init__(self,
                 timeout: int = 10,
                 phrase_time_limit: int = None,
                 pause_threshold: float = 2.0):
        super().__init__()

        self.timeout = timeout
        self.phrase_time_limit = phrase_time_limit
        self.pause_threshold = pause_threshold

    @override
    def __post_init__(self):
        super().__post_init__()

        self.recognizer = sr.Recognizer()
        self.recognizer.pause_threshold = self.pause_threshold

    @override
    @cached_property
    def source(self) -> sr.AudioSource:
        return sr.Microphone()

    @override
    def _listen(self) -> sr.AudioData:
        with self.source as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=0.2)

            logger.info('🎙️ Listening started...')

            audio = self.recognizer.listen(
                source,
                timeout=self.timeout,
                phrase_time_limit=self.phrase_time_limit,
            )

            logger.info('🎙️ Audio captured, processing...')

            return audio


speech_recognition_listener = SpeechRecognitionListener(timeout=10, pause_threshold=1.0)

__all__ = ['speech_recognition_listener']
