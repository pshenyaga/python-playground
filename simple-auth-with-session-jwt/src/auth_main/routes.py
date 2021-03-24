import aiohttp_jinja2

from aiohttp import web, log
from . import data_models


routes = web.RouteTableDef()
data_models.create_example_storage()

@routes.get('/', name='index')
@aiohttp_jinja2.template("index.j2")   
async def index(request: web.Request) -> dict:
    return {'is_authorized': True}

@routes.get('/login', name='login')
@aiohttp_jinja2.template("login.j2")
async def login_page(request: web.Request) -> dict:
    return {}

@routes.post('/login')
async def login(request: web.Request) -> None:
    router = request.app.router
    post_data = await request.post()
    user = None
    try:
        user: data_models.User = data_models.UserStorage.get_user(email = post_data.get('email', None))
        user.match_password(post_data.get('password', None))

    except (data_models.UserStorage.UserNotFound, data_models.User.PasswordDoesNotMatch) as e:
        log.server_logger.debug(e)
        raise web.HTTPFound(router['login'].url_for())        

    raise web.HTTPFound(router['index'].url_for())
