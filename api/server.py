from . import handlers
from sanic import Sanic

app = Sanic('api')

app.add_route(handlers.home, '/', name='Recommendations')
app.add_route(handlers.search, '/search', name='Search')
app.add_route(handlers.download, '/download', name='Download')
