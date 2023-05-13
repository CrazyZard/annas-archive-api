from dataclasses import dataclass


@dataclass
class FileInfo:
    name: str | None
    language: str | None
    extension: str
    size: str


def extract_file_info(raw: str) -> FileInfo:
    # sample data:
    #  English [en], pdf, 7.5MB, "Python_Web_Scraping_-_Second_Edition.pdf"
    #  English [en], pdf, 1.5MB
    #  mobi, 4.1MB
    info_list = raw.split(', ')
    language = None
    if '[' in info_list[0]:
        language = info_list.pop(0)
    extension = info_list.pop(0)
    size = info_list.pop(0)
    name = None
    if len(info_list) > 0:
        name = ", ".join(info_list).replace('"', '')
    return FileInfo(name, language, extension, size)
