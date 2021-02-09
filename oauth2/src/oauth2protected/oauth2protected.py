from aiohttp import web

from .routes import routes

def init_app() -> web.Application:
    _app: web.Application = web.Application()
    _app.add_routes(routes)

    return _app

def main():
    app: web.Application = init_app()
    web.run_app(app, host='127.0.0.1', port=9002)