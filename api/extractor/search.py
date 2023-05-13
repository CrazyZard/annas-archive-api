from .generic import FileInfo, extract_file_info
from .. import FRONT_PAGE
from ..utils import get
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
    authors: list[str]
    publisher: str
    publish_date: str
    thumbnail_url: str
    url: str
    file_info: FileInfo


async def get_search_results(query: str, language: str = "",
                             file_type: FileType = FileType.ANY,
                             order_by: OrderBy = OrderBy.MOST_RELEVANT) -> list[Result]:
    response = await get(
        url=f"{FRONT_PAGE}/search",
        params={
            'q': query,
            'lang': language,
            'ext': file_type.value,
            'sort': order_by.value
        }
    )
    soup = BeautifulSoup(response.text, 'lxml')
    raw_results = soup.find_all('div', class_='h-[125]')
    results = list(map(parse_result, raw_results))
    return [i for i in results if i != None]


def parse_result(raw_content: Tag) -> Result | None:
    try:
        title = raw_content.find('h3').get_text(strip=True)
    except:
        if '<!--' in str(raw_content):
            return parse_result(uncomment_tag(raw_content))
        return None
    authors = raw_content.find(
        'div',
        class_='truncate italic'
    ).get_text(strip=True).split(', ')
    publish_info = raw_content.find(
        'div', class_='truncate text-sm'
    ).text.split(', ')
    publisher = publish_info[0]
    publish_date = ', '.join(publish_info[1:])
    thumbnail_url = raw_content.find('img').get('src')
    url = raw_content.find('a').get('href')
    file_info = extract_file_info(
        raw_content.find('div', class_='truncate text-xs text-gray-500').text
    )
    return Result(
        title, authors, publisher, publish_date,
        thumbnail_url, url, file_info
    )


def uncomment_tag(tag: Tag) -> Tag:
    raw_tag = str(tag).replace('<!--', '').replace('-->', '')
    return BeautifulSoup(raw_tag, 'lxml')
