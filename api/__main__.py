from sanic import Sanic
from os import environ

server = Sanic(__name__)

server.run(
    host='0.0.0.0',
    port=int(environ.get('PORT', 8080))
)
