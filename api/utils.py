from time import time
from aiohttp import ClientSession
from dataclasses import dataclass
from sanic.request import Request
from sanic.response import HTTPResponse
from asyncio import create_task, sleep

CACHE_TIME = 10


@dataclass
class Cache:
    response: HTTPResponse
    expires: float


@dataclass
class Response:
    status_code: int
    text: str


async def http_get(url: str, params: dict = {}) -> Response:
    session = ClientSession()
    response = await session.get(url, params=params)
    text = await response.text()
    await session.close()
    return Response(response.status, text)


def cache(func):
    cache_storage: dict[str, Cache] = {}

    def remove_expired_items():
        for url, cache in cache_storage.items():
            if time() >= cache.expires:
                cache_storage.pop(url)

    async def clean_cache():
        while cache_storage:
            try:
                remove_expired_items()
            except:
                pass
            await sleep(1)

    async def wrapper(request: Request, *args, **kwargs) -> HTTPResponse:
        cached_data = cache_storage.get(request.url)

        if not cached_data or cached_data.expires < time():
            response = await func(request, *args, **kwargs)
            cache_storage[request.url] = Cache(response, time() + CACHE_TIME)
            cached_data = cache_storage[request.url]

        expires_in = int(cached_data.expires - time())
        cached_data.response.headers["Cache-Control"] = f"max-age={expires_in}"
        if len(cache_storage) == 1:
            create_task(clean_cache(), name=f'cacheCleaner:{func.__name__}')
        return cached_data.response
    return wrapper
