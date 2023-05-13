from .. import FRONT_PAGE
from ..utils import get
from bs4 import BeautifulSoup, Tag
from dataclasses import dataclass


@dataclass
class Recommendation:
    title: str
    authors: list[str]
    thumbnail_url: str
    url: str


async def get_recommendations():
    response = await get(FRONT_PAGE)
    soup = BeautifulSoup(response.text, 'lxml')
    recommendation_containers = soup.find_all('a', rel='nofollow')
    recommendations = list(
        map(parse_recommendation, recommendation_containers))
    return recommendations


def parse_recommendation(raw_content: Tag) -> Recommendation:
    title = raw_content.find('h3').get_text(strip=True)
    author_list = raw_content.find(
        'div', class_='text-lg italic').text.split(', ')
    thumbnail_url = raw_content.find('img').get('src')
    url = raw_content.get('href')
    return Recommendation(title, author_list, thumbnail_url, url)
