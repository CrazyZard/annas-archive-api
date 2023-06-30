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
    recommendations = list(map(
        parse_recommendation,
        soup.find_all('a', rel='nofollow')
    ))
    return [r for r in recommendations if r is not None]


def parse_recommendation(raw_content: Tag) -> Recommendation | None:
    try:
        recommendation = Recommendation(
            title=raw_content.find('h3').text,
            authors=raw_content.find('div', class_='text-lg italic').text,
            thumbnail=raw_content.find('img').get('src')
        )
    except:
        return None
    return recommendation
