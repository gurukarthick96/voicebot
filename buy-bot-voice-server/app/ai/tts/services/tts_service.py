from abc import ABC, abstractmethod

from app.utils import logger


class TTSService(ABC):

    def __init__(self):
        logger.info('initializing %s...', self.__class__.__name__)

    @abstractmethod
    def __post_init__(self):
        pass

    @abstractmethod
    def speak(self, texts: list[str]) -> None:
        pass

    @abstractmethod
    def synthesize(self, texts: list[str]) -> str:
        pass


__all__ = ['TTSService']
