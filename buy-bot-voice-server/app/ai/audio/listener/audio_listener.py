from abc import ABC, abstractmethod
from typing import Any, Optional

import speech_recognition as sr

from app.utils import logger


class AudioListener(ABC):

    def __init__(self):
        logger.info('initializing %s...', self.__class__.__name__)

    def __post_init__(self):
        pass

    @property
    @abstractmethod
    def source(self) -> Any:
        pass

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def __del__(self):
        self.cleanup()

    def cleanup(self):
        pass

    def listen(self) -> Optional[sr.AudioData]:
        try:
            return self._listen_or_raise()
        except:
            logger.error('unable to listen', exc_info=True)
            raise

    def _listen_or_raise(self) -> sr.AudioData:
        try:
            return self._listen()
        except sr.WaitTimeoutError:
            raise RuntimeError('timeout while listening')

    @abstractmethod
    def _listen(self) -> sr.AudioData:
        pass


__all__ = ['AudioListener']
