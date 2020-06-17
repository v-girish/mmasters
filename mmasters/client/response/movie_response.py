import logging
from http import HTTPStatus

import requests

from mmasters.client.model.movie import Movie, EmptyMovie
from mmasters.exception.exception import MovieClientException, MovieNotFoundException


class MovieResponse:

    def __init__(self, title: str, response: requests.Response):
        self.__title = title
        self.__response = response
        self.logger = logging.getLogger(__name__)

    def movie(self) -> Movie:
        try:
            self.__parse()
        except Exception:
            self.logger.exception(f"Error while fetching movie with title {self.__title}")
            return EmptyMovie(self.__title)

        return Movie.from_json(self.__response.json())

    def __parse(self):
        self.logger.info(f"Received status code for movie {self.__title} as {self.__response.status_code}")

        if self.__is_not_success_response():
            self.logger.error(f"Received error response for movie {self.__title}: {self.__response.text}")
            raise MovieClientException("Something went wrong")

        if self.__is_not_found_response():
            raise MovieNotFoundException(self.__title)

    def __is_not_success_response(self) -> bool:
        return self.__response.status_code != HTTPStatus.OK

    def __is_not_found_response(self) -> bool:
        return self.__response.json().get("Error") is not None
