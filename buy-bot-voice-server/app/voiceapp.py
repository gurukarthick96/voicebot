from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app import config
from app.api import lifespan, middleware
from app.api.exceptions.handlers import value_error_handler, generic_exception_handler
from app.api.routers import internal_router, bot_router, ui_router

app = FastAPI(
    root_path=config.BASE_PATH,
    lifespan=lifespan,
    middleware=middleware
)

app.include_router(internal_router)
app.include_router(bot_router)
app.include_router(ui_router)

app.add_exception_handler(ValueError, value_error_handler)
app.add_exception_handler(Exception, generic_exception_handler)

app.mount('/static', StaticFiles(directory='static'), name='static')


@app.get('/')
def root():
    return 'Welcome to Voice Bot!'


__all__ = ['app']
