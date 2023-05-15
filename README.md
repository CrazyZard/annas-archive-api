# Anna's Archive API

An unofficial API for the [Anna's Archive](https://annas-archive.org)
website made in python with coffee :)

Few to contribute to this project with code and relating problems or
just making a suggestion.


## Routes

### `/`: Get recommendations
  - Description: Get the recommendations from homepage of the website
  - Parameters: Don't need
  - Returns: A list of [Recommendations](api/extractor/home.py#L8)

### `/search`: Search for contents
  - Description: Search using filters and with a selectable sort
  - Parameters:
    - q: Query to search(required)
    - language: Language code
    - extension: File extension
    - sort: Sort order to be used(see the valid values [here](api/extractor/search.py#L9))
  - Returns: A list of [Result](api/extractor/search.py#L42)


### `/download`: Get content informations
  - Description: Get file informations like the basic informations, book description, and other file informations
  - Parameters:
    - `path`: The URL path to the content
  - Returns: [Download](api/extractor/download.py#L15)
