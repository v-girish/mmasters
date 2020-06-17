import logging

import requests

from mmasters.client.model.movie import Movie, EmptyMovie
from flask import current_app as app

from mmasters.client.response.movie_response import MovieResponse


class MovieClient:

    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def fetch(self, title: str) -> Movie:
        omdb_api_base_url = app.config.get('OMDB_API_BASE_URL')

        try:
            response = requests.get(omdb_api_base_url, params=self.__query_params(title))
        except requests.exceptions.RequestException as exception:
            self.logger.exception(f"Error while making request to fetch movie: {title}", exception)
            return EmptyMovie(title)

        return MovieResponse(title, response).movie()

    @staticmethod
    def __query_params(title):
        return {'t': title, 'apikey': (app.config.get('OMDB_API_KEY'))}


movie_client = MovieClient()
