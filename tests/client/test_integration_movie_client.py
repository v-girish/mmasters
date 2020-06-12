import unittest

import requests_mock

from mmasters.app import Application
from mmasters.client.model.movie import Movie
from mmasters.client.movie_client import movie_client
from mmasters.exception.exception import MovieNotFoundException, MovieClientException


class MovieClientIntegrationTest(unittest.TestCase):

    def setUp(self) -> None:
        self.app = Application.create_app({})
        self.app.config['OMDB_API_BASE_URL'] = 'http://localhost:9999/'
        self.app.config['OMDB_API_KEY'] = 'obmdb_api_key'
        self.app.app_context().push()

    @requests_mock.Mocker()
    def test_should_return_a_movie(self, mock_request):
        movie_json = """
            {
                "Title": "Dangal",
                "Year": "2009",
                "Released": "25 Dec 2009",
                "Director": "Rajkumar Hirani",
                "Ratings": [
                    {
                        "Source": "Internet Movie Database",
                        "Value": "8.4/10"
                    },
                    {
                        "Source": "Rotten Tomatoes",
                        "Value": "100%"
                    },
                    {
                        "Source": "Metacritic",
                        "Value": "67/100"
                    }
                ]
            }
        """
        mock_request.get(f'http://localhost:9999/?t=Dangal&apikey=obmdb_api_key', text=movie_json)

        actual_movie_response = movie_client.fetch_movies('Dangal')

        expected_movie = Movie("Dangal", "2009")
        self.assertEqual(expected_movie, actual_movie_response)

    @requests_mock.Mocker()
    def test_should_raise_movie_not_found_exception_when_movie_does_not_exist_with_that_title(self, mock_request):
        movie_not_found_response = """
            {
                "Response": "False",
                "Error": "Movie not found!"
            }
        """
        mock_request.get(f'http://localhost:9999/?t=UnkownMovie&apikey=obmdb_api_key', text=movie_not_found_response)

        with self.assertRaises(MovieNotFoundException) as context:
            movie_client.fetch_movies('UnkownMovie')

        self.assertEqual("Movie with title UnkownMovie not found", context.exception.message)

    @requests_mock.Mocker()
    def test_should_raise_movie_client_exception_when_api_response_is_unauthorized(self, mock_request):
        unauthorized_response = """
                {
                    "Response": "False",
                    "Error": "Invalid API Key!"
                }
            """
        mock_request.get(f'http://localhost:9999/?t=Dangal&apikey=obmdb_api_key',
                         text=unauthorized_response,
                         status_code=401)

        with self.assertRaises(MovieClientException) as context:
            movie_client.fetch_movies('Dangal')

        self.assertEqual("Something went wrong", context.exception.message)

    @requests_mock.Mocker()
    def test_should_raise_movie_client_exception_when_api_response_is_internal_server_error(self, mock_request):
        mock_request.get(f'http://localhost:9999/?t=Dangal&apikey=obmdb_api_key',
                         text="",
                         status_code=500)

        with self.assertRaises(MovieClientException) as context:
            movie_client.fetch_movies('Dangal')

        self.assertEqual("Something went wrong", context.exception.message)


