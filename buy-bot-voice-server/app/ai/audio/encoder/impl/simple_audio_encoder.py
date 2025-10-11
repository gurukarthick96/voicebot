import base64

from typing_extensions import override

from app.ai.audio.encoder import AudioEncoder
from app.utils import post_init, singleton


@singleton
@post_init
class SimpleAudioEncoder(AudioEncoder):

    @override
    def __init__(self, encoding: str = 'utf-8'):
        super().__init__()

        self.encoding = encoding

    @override
    def __post_init__(self):
        super().__post_init__()

    @override
    def _encode(self, audio_bytes: bytes) -> str:
        return base64.b64encode(audio_bytes).decode(self.encoding)


simple_audio_encoder = SimpleAudioEncoder()

__all__ = ['simple_audio_encoder']
