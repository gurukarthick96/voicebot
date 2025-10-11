from abc import ABC, abstractmethod
from typing import Optional

from app.utils import logger


class AudioEncoder(ABC):

    def __init__(self):
        logger.info('initializing %s...', self.__class__.__name__)

    def __post_init__(self):
        pass

    def encode(self, audio_bytes: bytes) -> Optional[str]:
        try:
            return self._encode(audio_bytes)
        except:
            logger.error('unable to encode', exc_info=True)
            raise

    @abstractmethod
    def _encode(self, audio_bytes: bytes) -> str:
        pass


__all__ = ['AudioEncoder']
