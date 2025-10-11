from app.env import get_env

ENVIRONMENT = get_env('ENVIRONMENT')

SERVICE_NAME = get_env('SERVICE_NAME', 'bot-action-server')

LOGGING_LEVEL = get_env('LOGGING_LEVEL', 'INFO')
LOGGING_FORMAT = '%(asctime)s %(levelname)s %(name)s %(filename)s:%(lineno)d -- %(message)s'

VECTOR_DB_URL = get_env('VECTOR_DB_URL')

GEMINI_API_KEY = get_env('GEMINI_API_KEY')
GEMINI_MODEL_NAME = get_env('GEMINI_MODEL_NAME')
TEXT_EMBEDDING_MODEL_NAME = get_env('TEXT_EMBEDDING_MODEL_NAME')
