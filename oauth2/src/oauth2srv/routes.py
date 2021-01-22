import aiohttp_jinja2
from aiohttp import web

routes = web.RouteTableDef()

@routes.get('/')
@aiohttp_jinja2.template('index.html.j2')
async def index(request: web.Request) -> web.Response:
    # return web.Response(text="OAuth2 server")
    return {}

@routes.get('/authorize')
@aiohttp_jinja2.template('authorize.html.j2')
async def authorize(request: web.Request) -> web.Response:
    clients_db: list = request.app['clients_db']
    
    response_type = request.query.get('response_type', None)
    client_id = request.query.get('client_id', None)
    redirect_uri = request.query.get('redirect_uri', None)

    if not response_type or not redirect_uri or not client_id:
        # Wrong request. Display error page
        raise web.HTTPBadRequest()

    client = next((c for c in clients_db if c['client_id'] == client_id), None)

    if not client:
        # Client unknown. Display error page.
        pass

    return { 'client_id': client['client_id'] }