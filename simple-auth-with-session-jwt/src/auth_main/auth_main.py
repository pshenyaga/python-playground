import jinja2
import aiohttp_jinja2
import logging
import base64


from aiohttp import web, log
from aiohttp_session import setup
from aiohttp_session.cookie_storage import EncryptedCookieStorage
from cryptography import fernet

from .routes import routes


def init_app() -> web.Application:
    _app = web.Application()
    _app.add_routes(routes)

    # aiohttp_session setup
    fernet_key = fernet.Fernet.generate_key()
    secret_key = base64.urlsafe_b64decode(fernet_key)
    setup(_app, EncryptedCookieStorage(fernet_key))

    # logging setup
    logging.basicConfig(level=logging.DEBUG)
    log.server_logger.setLevel(logging.DEBUG)

    # jinja2 template engine setup
    aiohttp_jinja2.setup(_app, loader=jinja2.PackageLoader('auth_main', 'templates'))

    return _app