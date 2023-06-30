from .generic import FileInfo, extract_file_info, extract_publish_info
from .. import FRONT_PAGE
from ..utils import http_get
from bs4 import BeautifulSoup, Tag
from dataclasses import dataclass
from enum import Enum


class OrderBy(Enum):
    MOST_RELEVANT = ''
    NEWEST = 'newest'
    OLDEST = 'oldest'
    LARGEST = 'largest'
    SMALLEST = 'smallest'


class FileType(Enum):
    ANY = ""
    PDF = "pdf"
    EPUB = "epub"
    MOBI = "mobi"
    AZW3 = "azw3"
    FB2 = "fb2"
    LIT = "lit"
    DJVU = "djvu"
    RTF = "rtf"
    ZIP = "zip"
    RAR = "rar"
    CBR = "cbr"
    TXT = "txt"
    CBZ = "cbz"
    HTML = "html"
    FB2_ZIP = "fb2.zip"
    DOC = "doc"
    HTM = "htm"
    DOCX = "docx"
    LRF = "lrf"
    MHT = "mht"


@dataclass
class Result:
    title: str
    authors: str
    publisher: str | None
    publish_date: str | None
    thumbnail: str | None
    path: str
    file_info: FileInfo


async def get_search_results(
        query: str, language: str = "",
        file_type: FileType = FileType.ANY,
        order_by: OrderBy = OrderBy.MOST_RELEVANT
) -> list[Result]:
    response = await http_get(
        url=f"{FRONT_PAGE}/search",
        params={
            'q': query,
            'lang': language,
            'ext': file_type.value,
            'sort': order_by.value
        }
    )
    html = response.text.replace('<!--', '').replace('-->', '')
    soup = BeautifulSoup(html, 'lxml')
    raw_results = soup.find_all('a', class_='js-vim-focus')
    results = list(map(parse_result, raw_results))
    return [i for i in results if i != None]


def parse_result(raw_content: Tag) -> Result | None:
    try:
        title = raw_content.find('h3').text.strip()
    except:
        return None
    authors = raw_content.find('div', class_='truncate italic').text

    publish_info = raw_content.find('div', class_='truncate text-sm').text
    publisher, publish_date = extract_publish_info(publish_info)

    thumbnail = raw_content.find('img').get('src') or None
    path = raw_content.get('href')

    raw_file_info = raw_content.find(
        'div',
        class_='truncate text-xs text-gray-500'
    ).text
    file_info = extract_file_info(raw_file_info)

    return Result(
        title, authors, publisher, publish_date,
        thumbnail, path, file_info
    )
