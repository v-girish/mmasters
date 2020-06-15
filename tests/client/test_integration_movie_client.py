import unittest

import requests_mock

from mmasters.app import Application
from mmasters.client.movie_client import movie_client
from mmasters.exception.exception import MovieNotFoundException, MovieClientException
from tests.builder.movies import Dangal
from tests.config.test_config import TestConfig
from tests.fixture.movie_client_mock_server import MovieClientMockServer


class MovieClientIntegrationTest(unittest.TestCase):

    def setUp(self) -> None:
        self.app = Application.create_app(TestConfig)
        self.app.config['OMDB_API_BASE_URL'] = 'http://localhost:9999/'
        self.app.config['OMDB_API_KEY'] = 'obmdb_api_key'
        self.app.app_context().push()
        self.movie_client_mock_server = MovieClientMockServer('http://localhost:9999/', 'obmdb_api_key')

    @requests_mock.Mocker()
    def test_should_return_a_movie(self, mock_request):
        self.movie_client_mock_server.success_response(mock_request, 'Dangal')

        actual_movie_response = movie_client.fetch('Dangal')

        self.assertEqual(Dangal, actual_movie_response)

    @requests_mock.Mocker()
    def test_should_raise_movie_not_found_exception_when_movie_does_not_exist_with_that_title(self, mock_request):
        self.movie_client_mock_server.not_found_response(mock_request, 'UnkownMovie')

        with self.assertRaises(MovieNotFoundException) as context:
            movie_client.fetch('UnkownMovie')

        self.assertEqual("Movie with title UnkownMovie not found", context.exception.message)

    @requests_mock.Mocker()
    def test_should_raise_movie_client_exception_when_api_response_is_unauthorized(self, mock_request):
        self.movie_client_mock_server.unauthorized_response(mock_request, 'Dangal')

        with self.assertRaises(MovieClientException) as context:
            movie_client.fetch('Dangal')

        self.assertEqual("Something went wrong", context.exception.message)

    @requests_mock.Mocker()
    def test_should_raise_movie_client_exception_when_api_response_is_internal_server_error(self, mock_request):
        self.movie_client_mock_server.server_error_response(mock_request, 'Dangal')

        with self.assertRaises(MovieClientException) as context:
            movie_client.fetch('Dangal')

        self.assertEqual("Something went wrong", context.exception.message)
