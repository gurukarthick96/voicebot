from fastapi import Request
from fastapi.responses import JSONResponse

from app.utils import logger


async def value_error_handler(request: Request, exception: ValueError):
    logger.error('caught value error: %s', str(exception))
    return JSONResponse(status_code=400, content={'error': str(exception)})


async def generic_exception_handler(request: Request, exception: Exception):
    logger.error('caught unhandled exception: %s', str(exception), exc_info=True)
    return JSONResponse(status_code=500, content={'error': str(exception)})


__all__ = ['value_error_handler', 'generic_exception_handler']
