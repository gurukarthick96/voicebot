from app.env import get_env

ENVIRONMENT = get_env('ENVIRONMENT')

SERVICE_NAME = get_env('SERVICE_NAME', 'bot-voice-server')
BASE_PATH = get_env('BASE_PATH', '/bot-voice-server')

SERVER_HOST = get_env('SERVER_HOST')
SERVER_PORT = get_env('SERVER_PORT', required_type=int)
SERVER_RELOAD = get_env('SERVER_RELOAD', False, required_type=bool)
SERVER_MAX_WORKERS = get_env('SERVER_MAX_WORKERS', 1, required_type=int)

LOGGING_LEVEL = get_env('LOGGING_LEVEL', 'INFO')
LOGGING_FORMAT = '%(asctime)s %(levelname)s %(name)s %(filename)s:%(lineno)d -- %(message)s'

BOT_CLIENT_BASE_URL = get_env('BOT_CLIENT_BASE_URL')
BOT_CLIENT_CHANNEL_NAME = get_env('BOT_CLIENT_CHANNEL_NAME')
