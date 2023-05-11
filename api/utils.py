from aiohttp import ClientSession
from dataclasses import dataclass


@dataclass
class Response:
    status_code: int
    text: str


async def get(url: str, params: dict = {}) -> Response:
    session = ClientSession()
    response = await session.get(url, params=params)
    text = await response.text()
    await session.close()
    return Response(response.status, text)
