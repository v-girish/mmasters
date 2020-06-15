import logging

import requests

from mmasters.client.model.movie import Movie
from flask import current_app as app

from mmasters.client.response.movie_response import MovieResponse


class MovieClient:

    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def fetch(self, title: str) -> Movie:
        omdb_api_base_url = app.config.get('OMDB_API_BASE_URL')

        response = requests.get(omdb_api_base_url, params=self.__query_params(title))

        return MovieResponse(title, response).movie()

    @staticmethod
    def __query_params(title):
        return {'t': title, 'apikey': (app.config.get('OMDB_API_KEY'))}


movie_client = MovieClient()
