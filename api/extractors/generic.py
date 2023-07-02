from dataclasses import dataclass


@dataclass
class FileInfo:
    language: str | None
    extension: str
    size: str


def extract_file_info(raw: str) -> FileInfo:
    # Extract file info from raw string given from the website
    # it assumes that the string will always have the file format
    # and size, but can have language and file name too
    # > Case one: Language, format, size and file name is provided;
    # > Case two: Language, format and size is provided, file name is omitted;
    # > Case three: Format and size is provided, language and name is omitted.

    # sample data:
    #  English [en], pdf, 7.5MB, "Python_Web_Scraping_-_Second_Edition.pdf"
    #  Portuguese [pt], epub, 1.5MB
    #  mobi, 4.1MB

    info_list = raw.split(', ')
    language = None
    if '[' in info_list[0]:
        language = info_list.pop(0)
    extension = info_list.pop(0)
    size = info_list.pop(0)
    return FileInfo(language, extension, size)


def extract_publish_info(raw: str) -> tuple[str | None, str | None]:
    # Sample data:
    #  John Wiley and Sons; Wiley (Blackwell Publishing); Blackwell Publishing Inc.; Wiley; JSTOR (ISSN 0020-6598), International Economic Review, #2, 45, pages 327-350, 2004 may
    #  Cambridge University Press, 10.1017/CBO9780511510854, 2001
    #  Cambridge University Press, 1, 2008
    #  Cambridge University Press, 2014 feb 16
    #  1, 2008
    #  2008

    if raw.strip() == '':
        return (None, None)
    info = [i for i in raw.split(', ') if i.strip()]
    last_info = info[-1].split()
    date = None
    if last_info[0].isdecimal() and last_info[0] != '0':
        info.pop()
        date = last_info.pop(0)
        if last_info:
            date = ' '.join(last_info) + ' of ' + date
        elif info and info[-1].isdecimal():
            date = info.pop() + ', ' + date
    publisher = ', '.join(info) or None
    return (publisher, date)
