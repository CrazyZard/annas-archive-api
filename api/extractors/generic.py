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
    #  1, 2008
    #  2008

    info = raw.split(', ')
    last_info = info[-1].split()
    publisher = None
    date = None

    if info[-1] == '0':
        # In this case the system don't know the date
        if len(info) > 1:
            publisher = ', '.join(info[:-1])
    elif last_info != []:
        if len(last_info) > 1 and last_info[0].isdecimal() and last_info[1].isalpha():
            # Month is in text format
            date = f'{last_info[1]} of {last_info[0]}'
            info.pop()
        # The system know the year and can know the month of publish
        if info[-1].isdecimal() and date is None:
            # System know both, year and month
            date = info.pop()
            if info[-1].isdecimal():
                date = info.pop() + ', ' + date
        publisher = ', '.join(info) or None
    elif info:
        # System don't know the date in any way
        publisher = ', '.join(info)
    return (publisher, date)
