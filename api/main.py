from sanic import Sanic
from . import routes

app = Sanic('api')
app.add_route(routes.home, '/')
app.add_route(routes.search, '/search')
