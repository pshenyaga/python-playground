import jinja2
import aiohttp_jinja2
import logging

from aiohttp import web, log

from .routes import routes


def init_app() -> web.Application:
    _app = web.Application()
    _app.add_routes(routes)
    logging.basicConfig(level=logging.DEBUG)
    log.server_logger.setLevel(logging.DEBUG)

    aiohttp_jinja2.setup(_app, loader=jinja2.PackageLoader('auth_main', 'templates'))

    return _app