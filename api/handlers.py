from . import extractors
from sanic.request import Request
from sanic.response import json
from dataclasses import asdict
from .utils import cache
from http import HTTPStatus
import logging


@cache
async def home(_):
    try:
        recommendations = await extractors.home.get_recommendations()
    except Exception as err:
        logging.error("loading recommendations", err)
        return json(
            body={'error': 'failed to load recommendations'},
            status=HTTPStatus.INTERNAL_SERVER_ERROR
        )
    response = json([asdict(r) for r in recommendations])
    return response


@cache
async def search(request: Request):
    query = request.args.get('q')
    if not query:
        return json(
            body={'error': 'missing query'},
            status=HTTPStatus.BAD_REQUEST
        )
    language = request.args.get('lang', '')
    extension = request.args.get('ext', '')
    order_by = request.args.get('sort', '')
    try:
        result = await extractors.search.get_search_results(
            query=query,
            language=language,
            file_type=extractors.search.FileType(extension),
            order_by=extractors.search.OrderBy(order_by)
        )
    except Exception as err:
        logging.error("searching", err)
        return json(
            body={'error': 'failed to load search results'},
            status=HTTPStatus.INTERNAL_SERVER_ERROR
        )
    response = json([asdict(r) for r in result])
    return response


@cache
async def download(request: Request):
    path = request.args.get('path')
    if not path:
        return json(
            body={'error': 'path parameter is missing'},
            status=HTTPStatus.BAD_REQUEST
        )
    try:
        download_data = await extractors.download.get_download(path)
    except Exception as err:
        logging.error("loading download information", err)
        return json(
            body={'error': 'failed to load download data'},
            status=HTTPStatus.INTERNAL_SERVER_ERROR
        )
    return json(asdict(download_data))
