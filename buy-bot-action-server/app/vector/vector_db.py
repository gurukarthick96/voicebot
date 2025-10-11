from qdrant_client import QdrantClient

from app import config
from app.utils import logger

vector_db_client = QdrantClient(location=config.VECTOR_DB_URL)

logger.info('connected to Vector DB on %s', config.VECTOR_DB_URL)

__all__ = ['vector_db_client']
