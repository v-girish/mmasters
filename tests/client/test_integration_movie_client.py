import unittest

import requests_mock

from mmasters.app import Application
from mmasters.client.model.movie import Rating, EmptyMovie
from mmasters.client.movie_client import movie_client
from tests.builder.movie_builder import MovieBuilder
from tests.config.test_config import TestConfig
from tests.fixture.movie_client_mock_server import MovieClientMockServer


class MovieClientIntegrationTest(unittest.TestCase):

    def setUp(self) -> None:
        self.app = Application.create_app(TestConfig)
        self.app.config['OMDB_API_BASE_URL'] = 'http://localhost:9999/'
        self.app.config['OMDB_API_KEY'] = 'omdb_api_key'
        self.app.app_context().push()
        self.movie_client_mock_server = MovieClientMockServer('http://localhost:9999/', 'omdb_api_key')

    @requests_mock.Mocker()
    def test_should_return_a_movie(self, mock_request):
        dangal_movie = MovieBuilder() \
            .with_title("Dangal") \
            .with_release_year("2009") \
            .with_release_date("25 Dec 2009") \
            .with_director("Rajkumar Hirani") \
            .with_ratings([Rating("Internet Movie Database", "8.4/10"), Rating("Rotten Tomatoes", "100%")]) \
            .build()

        self.movie_client_mock_server.success_response_with(mock_request, dangal_movie)

        actual_movie_response = movie_client.fetch('Dangal')

        expected_movie = MovieBuilder() \
            .with_title("Dangal") \
            .with_release_year("2009") \
            .with_release_date("25 Dec 2009") \
            .with_director("Rajkumar Hirani") \
            .with_ratings([Rating("Internet Movie Database", "8.4/10"), Rating("Rotten Tomatoes", "100%")]) \
            .build()

        self.assertEqual(expected_movie, actual_movie_response)

    @requests_mock.Mocker()
    def test_should_return_empty_movie_when_movie_does_not_exist_with_that_title(self, mock_request):
        self.movie_client_mock_server.not_found_response(mock_request, 'UnkownMovie')

        movie = movie_client.fetch('UnkownMovie')

        expected_movie = EmptyMovie("UnkownMovie")

        self.assertEqual(expected_movie, movie)

    @requests_mock.Mocker()
    def test_should_return_empty_movie_when_api_response_is_unauthorized(self, mock_request):
        self.movie_client_mock_server.unauthorized_response(mock_request, 'Dangal')

        movie = movie_client.fetch('Dangal')

        expected_movie = EmptyMovie("Dangal")

        self.assertEqual(expected_movie, movie)

    @requests_mock.Mocker()
    def test_should_return_empty_movie_when_api_response_is_internal_server_error(self, mock_request):
        self.movie_client_mock_server.server_error_response(mock_request, 'Dangal')

        movie = movie_client.fetch('Dangal')

        expected_movie = EmptyMovie("Dangal")

        self.assertEqual(expected_movie, movie)

    @requests_mock.Mocker()
    def test_should_return_empty_movie_when_request_fails_with_a_timeout_error(self, mock_request):
        self.movie_client_mock_server.timeout_error(mock_request, 'Dangal')

        movie = movie_client.fetch('Dangal')

        expected_movie = EmptyMovie("Dangal")

        self.assertEqual(expected_movie, movie)
