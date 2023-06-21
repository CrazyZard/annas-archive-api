from .extractor import home, search, download
from sanic.request import Request
from sanic.response import json
from dataclasses import asdict
from .utils import cache
import traceback
import sys


@cache
async def home_handler(_):
    try:
        recommendations = await home.get_recommendations()
    except Exception as err:
        return json({'error': 'failed to load recommendations: ' + str(err)}, status=500)
    recommendations_list = [asdict(r) for r in recommendations]
    return json(recommendations_list)


@cache
async def search_handler(request: Request):
    query = request.args.get('q')
    if not query:
        return json({'error': 'missing query'}, status=400)
    language = request.args.get('lang', '')
    extension = request.args.get('ext', '')
    order_by = request.args.get('sort', '')
    try:
        result = await search.get_search_results(
            query=query,
            language=language,
            file_type=search.FileType(extension),
            order_by=search.OrderBy(order_by)
        )
    except Exception as err:
        return json({'error': 'failed to load search results: ' + str(err)}, status=500)
    result_list = [asdict(r) for r in result]
    return json(result_list)


@cache
async def download_handler(request: Request):
    path = request.args.get('path')
    if not path:
        return json({'error': 'missing path'}, status=400)
    try:
        download_data = await download.get_download(path)
    except Exception as err:
        traceback.print_exc(file=sys.stdout)
        return json({'error': 'failed to load download data: ' + str(err)}, status=500)
    return json(asdict(download_data))
