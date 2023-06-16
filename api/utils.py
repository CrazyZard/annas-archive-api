from time import time
from aiohttp import ClientSession
from dataclasses import dataclass
from sanic.request import Request
from sanic.response import HTTPResponse
from asyncio import create_task, sleep

CACHE_TIME = 3600


@dataclass
class Response:
    status_code: int
    text: str


@dataclass
class Cache:
    response: HTTPResponse
    expires: float


async def get(url: str, params: dict = {}) -> Response:
    session = ClientSession()
    response = await session.get(url, params=params)
    text = await response.text()
    await session.close()
    return Response(response.status, text)


def cache(func):
    cache_storage: dict[str, Cache] = {}

    async def clean_cache():
        while len(cache_storage) > 0:
            try:
                print(func, len(cache_storage))
                for url, cache in cache_storage.items():
                    if time() >= cache.expires:
                        cache_storage.pop(url)
            except:
                continue
            await sleep(1)

    async def wrapper(request: Request, *args, **kwargs) -> HTTPResponse:
        cache_data = cache_storage.get(request.url)
        if not cache_data or cache_data.expires < time():
            response = await func(request, *args, **kwargs)
            cache_storage[request.url] = Cache(response, time() + CACHE_TIME)
            cache_data = cache_storage[request.url]
        expires_in = int(cache_data.expires - time())
        cache_data.response.headers["Cache-Control"] = f"max-age={expires_in}"
        if len(cache_storage) == 1:
            create_task(clean_cache())
        return cache_data.response
    return wrapper
