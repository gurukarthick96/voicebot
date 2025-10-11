import uvicorn

import app.config as config
from app.utils import logger


def run_locally():
    try:
        logger.info('starting app locally...')
        uvicorn.run(
            app='app:voiceapp',
            host=config.SERVER_HOST,
            port=config.SERVER_PORT,
            reload=config.SERVER_RELOAD,
            workers=config.SERVER_MAX_WORKERS,
            log_config=None
        )

    except Exception as e:
        logger.error('caught unexpected error: %s', str(e), exc_info=True)

    finally:
        logger.info('exiting app...')


if __name__ == '__main__':
    if config.ENVIRONMENT == 'local':
        run_locally()
    else:
        logger.warning('ENVIRONMENT has to be local')
