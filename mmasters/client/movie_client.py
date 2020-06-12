from http import HTTPStatus

import requests

from mmasters.client.model.movie import Movie
from flask import current_app as app

from mmasters.exception.exception import MovieNotFoundException, MovieClientException


class MovieClient:

    def fetch_movies(self, title: str) -> Movie:
        omdb_api_key = app.config.get('OMDB_API_KEY')
        omdb_api_base_url = app.config.get('OMDB_API_BASE_URL')
        query_params = {'t': title, 'apikey': omdb_api_key}

        response = requests.get(omdb_api_base_url, params=query_params)
        self.parse_response(response, title)

        return Movie.from_json(response.json())

    @staticmethod
    def parse_response(response, title):
        if response.status_code != HTTPStatus.OK:
            raise MovieClientException("Something went wrong")
        if response.json().get("Error") is not None:
            raise MovieNotFoundException(title)


movie_client = MovieClient()
