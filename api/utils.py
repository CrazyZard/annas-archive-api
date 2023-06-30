from time import time
from aiohttp import request
from dataclasses import dataclass
from sanic.request import Request
from sanic.response import HTTPResponse
from asyncio import create_task, sleep

CACHE_TIMEOUT = 30 * 60
ERROR_CACHED_TIMEOUT = 1 * 60


@dataclass
class Cache:
    response: HTTPResponse
    expires: float


@dataclass
class Response:
    status_code: int
    text: str


async def http_get(url: str, params: dict = {}) -> Response:
    async with request('GET', url, params=params) as response:
        text = await response.text()
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

        if not cached_data:
            response = await func(request, *args, **kwargs)
            expires_at = time() + (CACHE_TIMEOUT if response.status < 500
                                   else ERROR_CACHED_TIMEOUT)
            cache_storage[request.url] = Cache(response, expires_at)
            cached_data = cache_storage[request.url]
            if len(cache_storage) == 1:
                create_task(
                    coro=clean_cache(),
                    name=f'cacheCleaner:{func.__name__}'
                )

        expires_in = int(cached_data.expires - time())
        cached_data.response.headers["Cache-Control"] = f"max-age={expires_in}"
        return cached_data.response

    return wrapper
