from .generic import FileInfo, extract_file_info, extract_publish_info
from .. import FRONT_PAGE
from ..utils import http_get
from bs4 import BeautifulSoup, Tag
from dataclasses import dataclass


@dataclass
class Link:
    title: str
    url: str


@dataclass
class Download:
    title: str
    authors: str
    description: str
    publisher: str | None
    publish_date: str | None
    thumbnail: str | None
    file_info: FileInfo
    download_links: list[Link]


async def get_download(path: str) -> Download:
    path = path if path[0] != '/' else path[1:]
    response = await http_get(f"{FRONT_PAGE}/{path}")
    soup = BeautifulSoup(response.text, 'lxml')

    clear = lambda s: s.replace('🔍', '').strip()

    title = clear(soup.find('div', class_='text-3xl font-bold').text)
    authors = clear(soup.find('div', class_='italic').text)
    description = soup.find(
        name='div',
        class_='js-md5-top-box-description'
    ).text
    thumbnail = soup.find('img').get('src') or None

    publish_info = soup.find('div', class_='text-md').text
    publisher, publish_date = extract_publish_info(publish_info)

    raw_file_info = soup.find('div', class_='text-sm text-gray-500').text
    file_info = extract_file_info(raw_file_info)
    download_links = list(map(
        parse_link,
        soup.find_all('a', class_='js-download-link')
    ))

    return Download(
        title, authors, description[1:-1], publisher,
        publish_date, thumbnail, file_info, download_links
    )


def parse_link(link: Tag) -> Link:
    return Link(
        title=link.text,
        url=link.get('href')
    )
