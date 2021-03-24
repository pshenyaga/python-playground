
from aiohttp import web

def init_app() -> web.Application:
    return web.Application()