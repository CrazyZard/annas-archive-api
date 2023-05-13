from .generic import FileInfo, extract_file_info
from .. import FRONT_PAGE
from ..utils import get
from bs4 import BeautifulSoup, Tag
from dataclasses import dataclass


@dataclass
class Link:
    title: str
    url: str


@dataclass
class Download:
    title: str
    authors: list[str]
    description: str
    publisher: str
    publish_date: str
    thumbnail_url: str
    file_info: FileInfo
    download_links: list[Link]


async def get_download(path: str) -> Download:
    path = path[1:] if path[0] == '/' else path
    response = await get(f"{FRONT_PAGE}/{path}")
    soup = BeautifulSoup(response.text, 'lxml')

    title = soup.find('div', class_='text-3xl font-bold').get_text(strip=True)
    authors = soup.find('div', class_='italic').get_text(
        strip=True).split(', ')
    description = soup.find(
        'div', class_='mt-4 line-clamp-[6]').get_text(strip=True)
    publish_info = soup.find('div', class_='text-md').text.split(', ')

    publisher = publish_info[0]
    publish_date = ', '.join(publish_info[1:])
    thumbnail_url = soup.find('img').get('src')
    file_info = extract_file_info(
        soup.find('div', class_='text-sm text-gray-500').text)
    download_links = list(
        map(parse_link, soup.find_all('a', class_='js-download-link')))

    return Download(title, authors, description[1:-1], publisher, publish_date, thumbnail_url, file_info, download_links)


def parse_link(link: Tag) -> Link:
    return Link(
        title=link.get_text(strip=True),
        url=link.get('href')
    )
