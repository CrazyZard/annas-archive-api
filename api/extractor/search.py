from .. import FRONT_PAGE
from ..utils import get
from bs4 import BeautifulSoup, NavigableString
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
class FileInfo:
    name: str
    language: str
    extension: str
    size: str


@dataclass
class Result:
    title: str
    authors: list[str]
    publisher: str
    publish_date: str
    thumbnail_url: str
    url: str
    file_info: FileInfo


async def getSearchResults(query: str, language: str = "",
                           file_type: FileType = FileType.ANY,
                           order_by: OrderBy = OrderBy.MOST_RELEVANT) -> list[Result]:
    response = await get(
        url=f"{FRONT_PAGE}/search",
        params={
            'q': query,
            'lang': language,
            'ext': file_type,
            'sort': order_by
        }
    )
    html = BeautifulSoup(response.text, 'lxml')
    raw_results = html.findAll('div', class_='h-[125]')
    results = list(map(parseResult, raw_results))
    return results


def parseResult(raw_content: NavigableString) -> Result:
    pass
