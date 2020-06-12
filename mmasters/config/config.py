from os import environ


class Config:
    API_KEY = environ.get('API_KEY')
    OMDB_API_KEY = environ.get('OMDB_API_KEY')
    OMDB_API_BASE_URL = "http://www.omdbapi.com/"
