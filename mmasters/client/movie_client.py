import json

import requests

from mmasters.client.model.movie import Movie


class MovieClient:

    def fetch_movies(self, title: str):
        query_params = {'t': title, 'apikey': 'abc'}
        response = requests.get("http://www.omdbapi.com/", params=query_params).json()
        return Movie.from_json(response)


movie_client = MovieClient()
