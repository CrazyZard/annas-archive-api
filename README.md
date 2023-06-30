# Anna's Archive API

An unofficial API for the [Anna's Archive](https://annas-archive.org)
website made in python with coffee :)

Feel free to contribute here with code and relating problems or
just making a suggestion.


## Routes

### `/`: Get recommendations
  - Description: Get the recommendations from homepage of the website
  - Parameters: Don't need
  - Returns: A list of [Recommendations](api/extractors/home.py#L8)

### `/search`: Search for contents
  - Description: Search using filters and with a selectable sort
  - Parameters:
    - q: Query to search(required)
    - lang: Language code
    - ext: File extension
    - sort: Sort order to be used(see the valid values [here](api/extractors/search.py#L9))
  - Returns: A list of [Result](api/extractors/search.py#L42)


### `/download`: Get content information
  - Description: Get file information like the basic information, book description, and other file information
  - Parameters:
    - `path`: The URL path to the content(required)
  - Returns: [Download](api/extractors/download.py#L15)
