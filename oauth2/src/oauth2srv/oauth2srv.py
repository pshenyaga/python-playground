import aiohttp_jinja2
import jinja2

from aiohttp import web

from .routes import routes

clients = [
    {
        'client_id': 'oauth-client-1',
        'client_secret': 'oauth-client-secret-1',
        'redirect_uris': ['http://localhost:9000/callback']
    }
]

def init_app(_clients: dict) -> web.Application:
    _app = web.Application()

    # jinja2 template renderer
    aiohttp_jinja2.setup(_app, loader=jinja2.PackageLoader('oauth2srv', 'templates'))
    
    _app.add_routes(routes)
    _app['clients_db'] = _clients

    return _app

def main():
    app = init_app(clients)
    web.run_app(app, host='127.0.0.1', port=9001)