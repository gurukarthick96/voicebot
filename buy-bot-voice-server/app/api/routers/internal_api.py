import socket

from fastapi import APIRouter, Depends

from app.bot.client.impl import bot_client

router = APIRouter(prefix='/internal')


@router.get('/ping')
def ping():
    return {
        'healthy': True,
        'hostname': socket.gethostname()
    }


async def check_bot_client_healthy():
    try:
        bot_client.health_check()
        return True
    except:
        return False


@router.get('/health')
async def health_check(bot_client_healthy: bool = Depends(check_bot_client_healthy)):
    return {
        'healthy': True if bot_client_healthy else False,
        'bot_client_healthy': bot_client_healthy,
        'hostname': socket.gethostname(),
    }


__all__ = ['router']
