from .extractor import home, search, download
from sanic.request import Request
from sanic.response import json
from dataclasses import asdict


async def home_handler(_):
    recommendations = await home.get_recommendations()
    recommendations_list = [asdict(r) for r in recommendations]
    return json(recommendations_list)


async def search_handler(request: Request):
    query = request.args.get('q')
    if not query:
        return json({'error': 'missing query'}, status=400)
    language = request.args.get('lang', '')
    extension = request.args.get('ext', '')
    order_by = request.args.get('sort', '')
    result = await search.get_search_results(
        query=query,
        language=language,
        file_type=search.FileType(extension),
        order_by=search.OrderBy(order_by)
    )
    result_list = [asdict(r) for r in result]
    return json(result_list)


async def download_handler(request: Request):
    path = request.args.get('path')
    if not path:
        return json({'error': 'missing path'}, status=400)
    download_data = await download.get_download(path)
    return json(asdict(download_data))
