from abc import ABC, abstractmethod

from app.utils import logger


class AudioDecoder(ABC):

    def __init__(self):
        logger.info('initializing %s...', self.__class__.__name__)

    def __post_init__(self):
        pass

    def decode(self, encoded_audio: str) -> bytes:
        if not encoded_audio:
            raise RuntimeError('encoded audio is empty')

        try:
            return self._decode(encoded_audio)
        except:
            logger.error('unable to decode', exc_info=True)
            raise

    @abstractmethod
    def _decode(self, encoded_audio: str) -> bytes:
        pass


__all__ = ['AudioDecoder']
