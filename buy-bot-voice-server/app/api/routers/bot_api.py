from fastapi import APIRouter

from app.api.handlers import bot_query_handler
from app.api.models import BotQueryRequest, BotQueryResponse

router = APIRouter(prefix='/bot')


@router.post('/query', response_model=BotQueryResponse)
async def query(request: BotQueryRequest):
    return bot_query_handler.handle_query(request)


__all__ = ['router']
