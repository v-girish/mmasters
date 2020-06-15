class MovieClientMockServer:

    def __init__(self, base_url: str, api_key: str):
        self.__base_url = base_url
        self.__api_key = api_key

    def success_response(self, mock_request, title: str):
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
                            }
                        ]
                    }
                """
        mock_request.get(f'{self.__base_url}?t={title}&apikey={self.__api_key}', text=movie_json)

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
