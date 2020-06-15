import logging
from http import HTTPStatus

import requests

from mmasters.client.model.movie import Movie
from flask import current_app as app

from mmasters.exception.exception import MovieNotFoundException, MovieClientException


class MovieClient:

    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def fetch_movies(self, title: str) -> Movie:
        omdb_api_key = app.config.get('OMDB_API_KEY')
        omdb_api_base_url = app.config.get('OMDB_API_BASE_URL')
        query_params = {'t': title, 'apikey': omdb_api_key}

        response = requests.get(omdb_api_base_url, params=query_params)
        self.parse_response(response, title)

        return Movie.from_json(response.json())

    def parse_response(self, response, title):
        self.logger.info(f"Received status code for movie {title} as {response.status_code}")
        if response.status_code != HTTPStatus.OK:
            self.logger.error(f"Received error response for movie {title}: {response.text}")
            raise MovieClientException("Something went wrong")
        if response.json().get("Error") is not None:
            raise MovieNotFoundException(title)


movie_client = MovieClient()
