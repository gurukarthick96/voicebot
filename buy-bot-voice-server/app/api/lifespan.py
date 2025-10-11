from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.ai.audio.decoder.impl import audio_decoder
from app.ai.audio.encoder.impl import audio_encoder
from app.ai.stt.services.impl import stt_service
from app.ai.tts.services.impl import tts_service
from app.utils import logger


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info('loading app...')

    try:
        logger.info('initialized %s.', audio_decoder.__class__.__name__)
        logger.info('initialized %s.', audio_encoder.__class__.__name__)
        logger.info('initialized %s.', stt_service.__class__.__name__)
        logger.info('initialized %s.', tts_service.__class__.__name__)

        yield
    finally:
        logger.info('unloading app...')


__all__ = ['lifespan']
