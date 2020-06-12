import requests

from mmasters.client.model.movie import Movie
from flask import current_app as app


class MovieClient:

    def fetch_movies(self, title: str):
        omdb_api_key = app.config.get('OMDB_API_KEY')
        omdb_api_base_url = app.config.get('OMDB_API_BASE_URL')
        query_params = {'t': title, 'apikey': omdb_api_key}

        response = requests.get(omdb_api_base_url, params=query_params).json()
        return Movie.from_json(response)


movie_client = MovieClient()
