import json

import requests

from mmasters.client.model.movie import Movie


class MovieClientMockServer:

    def __init__(self, base_url: str, api_key: str):
        self.__base_url = base_url
        self.__api_key = api_key

    def success_response_with(self, mock_request, movie: Movie):
        movie_json = json.dumps({
            "Title": movie.title,
            "Year": movie.release_year,
            "Released": movie.release_date,
            "Director": movie.director,
            "Ratings": [
                {
                    "Source": movie.ratings[0].source,
                    "Value": movie.ratings[0].value
                },
                {
                    "Source": movie.ratings[1].source,
                    "Value": movie.ratings[1].value
                }
            ]
        })

        mock_request.get(f'{self.__base_url}?t={movie.title}&apikey={self.__api_key}', text=movie_json)

    def not_found_response(self, mock_request, title: str):
        movie_not_found_response = """
                    {
                        "Response": "False",
                        "Error": "Movie not found!"
                    }
                """
        mock_request.get(f'{self.__base_url}?t={title}&apikey={self.__api_key}', text=movie_not_found_response,
                         status_code=200)

    def unauthorized_response(self, mock_request, title: str):
        unauthorized_response = """
                        {
                            "Response": "False",
                            "Error": "Invalid API Key!"
                        }
                    """
        mock_request.get(f'{self.__base_url}?t={title}&apikey={self.__api_key}',
                         text=unauthorized_response,
                         status_code=401)

    def server_error_response(self, mock_request, title: str):
        mock_request.get(f'{self.__base_url}?t={title}&apikey={self.__api_key}',
                         text="Internal Server Error",
                         status_code=500)

    def timeout_error(self, mock_request, title: str):
        mock_request.get(f'{self.__base_url}?t={title}&apikey={self.__api_key}',
                         exc=requests.exceptions.Timeout)
