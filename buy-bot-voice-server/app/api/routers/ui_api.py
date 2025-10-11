from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, PlainTextResponse
from fastapi.templating import Jinja2Templates

from app import config

router = APIRouter(prefix='/ui')

templates = Jinja2Templates(directory='templates')


@router.get(path='', response_class=HTMLResponse)
def get_ui(request: Request):
    return templates.TemplateResponse(
        request=request,
        name='index.html',
        context={}
    )


@router.get('/config.js', response_class=PlainTextResponse)
def get_config_js():
    js = f'window.appConfig = {{ BASE_PATH: "{config.BASE_PATH}" }};'
    return js


__all__ = ['router']
