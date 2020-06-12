import unittest

import requests_mock

from mmasters.client.model.movie import Movie
from mmasters.client.movie_client import movie_client


class MovieClientIntegrationTest(unittest.TestCase):

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
        mock_request.get('http://www.omdbapi.com/?t=Dangal&apikey=abc', text=movie_json)

        actual_movie_response = movie_client.fetch_movies('Dangal')

        expected_movie = Movie("Dangal", "2009")
        self.assertEqual(expected_movie, actual_movie_response)
