import aiohttp_jinja2

from aiohttp import web
from oauth2helpers import build_url

routes = web.RouteTableDef()

@routes.get('/')
@aiohttp_jinja2.template('index.html.j2')
async def index(Request: web.Request) -> web.Response:
    # app = Request.app
    return {}

@routes.get('/authorize')
async def authorize(Request: web.Request) -> web.Response:
    app = Request.app
    client_config = app['config']['client']
    auth_server_config = app['config']['auth_server']
    authorize_url = build_url(
        auth_server_config['authorization_endpoint'],
        {
            'response_type': 'code',
            'client_id': client_config['client_id'],
            'redirect_uri': client_config['redirect_uris'][0]
        })

    raise web.HTTPFound(location=authorize_url)
