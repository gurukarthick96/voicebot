import logging
import logging.handlers
import os

import coloredlogs

from app import config

LOG_DIR = 'logs'
LOG_FILE = os.path.join(LOG_DIR, 'app.log')

os.makedirs(LOG_DIR, exist_ok=True)


def get_global_logger():
    app_logger = logging.getLogger(config.SERVICE_NAME)

    configure_loggers([app_logger])

    return app_logger


def configure_loggers(loggers: list[logging.Logger]) -> None:
    if loggers[0].hasHandlers():
        return

    formatter = logging.Formatter(config.LOGGING_FORMAT)

    file_handler = logging.handlers.RotatingFileHandler(LOG_FILE, maxBytes=10 * 1024 * 1024, backupCount=3)
    file_handler.setFormatter(formatter)

    for _logger in loggers:
        _logger.setLevel(config.LOGGING_LEVEL)
        _logger.addHandler(file_handler)
        coloredlogs.install(level=config.LOGGING_LEVEL, logger=_logger, fmt=config.LOGGING_FORMAT)


logger = get_global_logger()

logger.info('logger initialized successfully...')

__all__ = ['logger']
