import aiohttp_jinja2

from aiohttp import web

routes = web.RouteTableDef()

@routes.get('/')
@aiohttp_jinja2.template('index.html.j2')
def index(Request: web.Request):
    # return web.Response(text="OAuth client")
    return {}

@routes.get('/authorize')
def authorize(Request: web.Request):
    pass