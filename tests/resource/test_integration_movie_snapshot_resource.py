import unittest

import requests_mock

from mmasters.app import Application
from mmasters.config.db_config import db
from mmasters.entity.movie_snapshot import Rating, MovieSnapshot
from tests.config.test_config import TestConfig


def authorization_header():
    return {'x-api-key': TestConfig.API_KEY}


class MovieSnapshotResourceIntegrationTest(unittest.TestCase):

    def setUp(self):
        self.app = Application.create_app(TestConfig)
        self.test_client = self.app.test_client()
        self.app.config['OMDB_API_BASE_URL'] = 'http://localhost:9999/'
        self.app.config['OMDB_API_KEY'] = 'obmdb_api_key'
        self.app.app_context().push()
        Rating.query.delete()
        MovieSnapshot.query.delete()

    @requests_mock.Mocker()
    def test_should_return_created_movie_snapshots(self, mock_request):
        self.mock_movie_api_success_response(mock_request)
        response = self.test_client.post("/movies-snapshots",
                                         json={"titles": ['Dangal']},
                                         headers=authorization_header())

        expected_json = [{'director': 'Rajkumar Hirani',
                          'ratings': [{'source': 'Internet Movie Database', 'value': '8.4/10'},
                                      {'source': 'Rotten Tomatoes', 'value': '100%'}],
                          'releaseDate': '25 Dec 2009',
                          'releaseYear': '2009',
                          'title': 'Dangal'}]
        self.assertEqual(201, response.status_code)
        self.assertEqual(expected_json, response.get_json())

        saved_movie_snapshots = MovieSnapshot.query.all()
        self.assertEqual(1, len(saved_movie_snapshots))

        saved_movie = saved_movie_snapshots[0]

        self.assertEqual('Dangal', saved_movie.title)
        self.assertEqual('2009', saved_movie.release_year)
        self.assertEqual('25 Dec 2009', saved_movie.release_date)
        self.assertEqual('Rajkumar Hirani', saved_movie.director)
        self.assertEqual('Internet Movie Database', saved_movie.ratings[0].source)
        self.assertEqual('8.4/10', saved_movie.ratings[0].value)
        self.assertEqual('Rotten Tomatoes', saved_movie.ratings[1].source)
        self.assertEqual('100%', saved_movie.ratings[1].value)

    def test_should_get_all_movie_snapshots(self):
        ratings = Rating(source='Internet Movie Database', value='8.4/10')
        movie_snapshot = MovieSnapshot(title="3 Idiots",
                                       release_year="2009",
                                       release_date='25 Dec 2009',
                                       director='Rajkumar Hirani',
                                       ratings=[ratings])

        db.session.add(movie_snapshot)
        db.session.commit()

        response = self.test_client.get("/movies-snapshots")

        expected_json = [{'director': 'Rajkumar Hirani',
                          'ratings': [{'source': 'Internet Movie Database', 'value': '8.4/10'}],
                          'releaseDate': '25 Dec 2009',
                          'releaseYear': '2009',
                          'title': '3 Idiots'}]
        self.assertEqual(200, response.status_code)
        self.assertEqual(expected_json, response.get_json())

    def mock_movie_api_success_response(self, mock_request):
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
        mock_request.get(f'http://localhost:9999/?t=Dangal&apikey=obmdb_api_key', text=movie_json)
