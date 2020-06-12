from os import environ


class Config:
    API_KEY = environ.get('API_KEY')
