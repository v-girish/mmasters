import logging
from http import HTTPStatus

import requests

from mmasters.client.model.movie import Movie, EmptyMovie


class MovieResponse:

    def __init__(self, title: str, response: requests.Response):
        self.__title = title
        self.__response = response
        self.logger = logging.getLogger(__name__)

    def movie(self) -> Movie:
        self.logger.info(f"Received status code for movie {self.__title} as {self.__response.status_code}")

        if self.__is_not_found_response():
            self.logger.error(f"Received error response for movie {self.__title}: {self.__response.text}")
            return EmptyMovie(self.__title)

        return Movie.from_json(self.__response.json())

    def __is_not_found_response(self) -> bool:
        return self.__response.json().get("Error") is not None
