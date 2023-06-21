from .. import FRONT_PAGE
from ..utils import http_get
from bs4 import BeautifulSoup, Tag
from dataclasses import dataclass


@dataclass
class Recommendation:
    title: str
    authors: str
    thumbnail: str


async def get_recommendations() -> list[Recommendation]:
    response = await http_get(FRONT_PAGE)
    soup = BeautifulSoup(response.text, 'lxml')
    recommendation_containers = soup.find_all('a', rel='nofollow')
    recommendations = map(parse_recommendation, recommendation_containers)
    return list(recommendations)


def parse_recommendation(raw_content: Tag) -> Recommendation:
    title = raw_content.find('h3').text
    authors = raw_content.find('div', class_='text-lg italic').text
    thumbnail_url = raw_content.find('img').get('src')
    return Recommendation(title, authors, thumbnail_url)
