from sanic.request import Request
from sanic.response import json
from .extractor.home import get_recommendations
from .extractor.search import getSearchResults
from dataclasses import asdict


async def home(_):
    recommendations = await get_recommendations()
    recommendations_list = [asdict(r) for r in recommendations]
    return json(recommendations_list)


async def search(request: Request):
    query = request.args.get('q')
    result = await getSearchResults(query)
    result_list = [asdict(r) for r in result]
    return json(result_list)
