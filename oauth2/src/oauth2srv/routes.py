import aiohttp_jinja2
from aiohttp import web

routes = web.RouteTableDef()

@routes.get('/')
@aiohttp_jinja2.template('index.html.j2')
async def index(request: web.Request) -> web.Response:
    # return web.Response(text="OAuth2 server")
    return {}