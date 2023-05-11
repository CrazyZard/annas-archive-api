from bs4 import BeautifulSoup, NavigableString
from ..utils import get
from .. import FRONT_PAGE
from dataclasses import dataclass


@dataclass
class Recommendation:
    title: str
    authors: list[str]
    thumbnail_url: str
    url: str


async def getRecommendations():
    response = await get(FRONT_PAGE)
    html = BeautifulSoup(response.text, 'lxml')
    raw_recommendations = html.findAll('a', rel='nofollow')
    recommendations = list(map(parseRecommendation, raw_recommendations))
    return recommendations


def parseRecommendation(raw_content: NavigableString) -> Recommendation:
    title = raw_content.find('h3').getText(strip=True)
    authors = raw_content.find('div', class_='text-lg italic').text.split(', ')
    thumbnail_url = raw_content.find('img').get('src')
    url = raw_content.get('href')
    return Recommendation(title, authors, thumbnail_url, url)
