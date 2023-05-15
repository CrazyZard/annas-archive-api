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
    # Get webpage and turn it into a BeautifulSoup object
    path = path[1:] if path[0] == '/' else path
    response = await get(f"{FRONT_PAGE}/{path}")
    soup = BeautifulSoup(response.text, 'lxml')

    # Extract basic data
    title = soup.find('div', class_='text-3xl font-bold').text
    authors = soup.find('div', class_='italic').text.split(', ')
    description = soup.find('div', class_='mt-4 line-clamp-[6]').text
    thumbnail_url = soup.find('img').get('src')

    # Extract publisher info using a basic logic
    publish_info = soup.find('div', class_='text-md').text.split(', ')
    publisher = publish_info[0]
    publish_date = ', '.join(publish_info[1:])

    # Extract file & download info processing data into dataclasses
    raw_file_info = soup.find('div', class_='text-sm text-gray-500').text
    file_info = extract_file_info(raw_file_info)
    download_links = list(map(
        parse_link,
        soup.find_all('a', class_='js-download-link')
    ))

    return Download(
        title, authors, description[1:-1], publisher,
        publish_date, thumbnail_url, file_info, download_links
    )


def parse_link(link: Tag) -> Link:
    return Link(
        title=link.text,
        url=link.get('href')
    )
