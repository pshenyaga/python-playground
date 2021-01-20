import aiohttp_jinja2
import jinja2

from aiohttp import web

from .routes import routes

def init_app() -> web.Application:
    _app = web.Application()

    # jinja2 template renderer
    aiohttp_jinja2.setup(_app, loader=jinja2.PackageLoader('oauth2srv', 'templates'))
    
    _app.add_routes(routes)

    return _app

def main():
    app = init_app()
    web.run_app(app, host='127.0.0.1', port=9001)