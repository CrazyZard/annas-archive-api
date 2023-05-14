from sanic import Sanic
from . import routes

app = Sanic('api')
app.add_route(routes.home_handler, '/', name="home")
app.add_route(routes.search_handler, '/search', name="search")
app.add_route(routes.download_handler, '/download', name="download")
