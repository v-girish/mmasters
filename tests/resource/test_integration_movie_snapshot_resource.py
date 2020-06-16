import unittest
from unittest import mock

import requests_mock

from mmasters.app import Application
from mmasters.client.model.movie import Rating
from mmasters.entity.movie_snapshot import RatingEntity, MovieSnapshotEntity
from tests.builder.movie_builder import MovieBuilder
from tests.config.test_config import TestConfig
from tests.fixture.movie_client_mock_server import MovieClientMockServer
from tests.fixture.movie_snapshot_fixture import MovieSnapshotFixture


def authorization_header():
    return {'x-api-key': TestConfig.API_KEY}


class MovieSnapshotResourceIntegrationTest(unittest.TestCase):

    def setUp(self):
        self.app = Application.create_app(TestConfig)
        self.test_client = self.app.test_client()

        self.app.config['OMDB_API_BASE_URL'] = 'http://localhost:9999/'
        self.app.config['OMDB_API_KEY'] = 'omdb_api_key'

        self.movie_client_mock_server = MovieClientMockServer('http://localhost:9999/', 'omdb_api_key')

        self.app.app_context().push()
        MovieSnapshotFixture().delete_all()

    @requests_mock.Mocker()
    def test_should_return_movie_snapshots_of_newly_created_movies(self, mock_request):
        dangal_movie = MovieBuilder() \
            .with_title("Dangal") \
            .with_release_year("2009") \
            .with_release_date("25 Dec 2009") \
            .with_director("Rajkumar Hirani") \
            .with_ratings([Rating("Internet Movie Database", "8.4/10"), Rating("Rotten Tomatoes", "100%")]) \
            .build()

        self.movie_client_mock_server.success_response_with(mock_request, dangal_movie)
        response = self.test_client.post("/movies-snapshots",
                                         json={"titles": ['Dangal']},
                                         headers=authorization_header())

        expected_json = [
            {
                'director': 'Rajkumar Hirani',
                'ratings': [
                    {'source': 'Internet Movie Database', 'value': '8.4/10'},
                    {'source': 'Rotten Tomatoes', 'value': '100%'}
                ],
                'releaseDate': '25 Dec 2009',
                'releaseYear': '2009',
                'title': 'Dangal',
                'id': mock.ANY,
                'is_empty': False
            }
        ]
        self.assertEqual(201, response.status_code)
        self.assertEqual(expected_json, response.get_json())

        saved_movie_snapshots = MovieSnapshotFixture.find_all()
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

    @requests_mock.Mocker()
    def test_should_return_empty_movie_snapshots_when_unable_to_fetch_movie(self, mock_request):
        dangal_movie = MovieBuilder() \
            .with_title("Dangal") \
            .with_release_year("2009") \
            .with_release_date("25 Dec 2009") \
            .with_director("Rajkumar Hirani") \
            .with_ratings([Rating("Internet Movie Database", "8.4/10"), Rating("Rotten Tomatoes", "100%")]) \
            .build()

        self.movie_client_mock_server.success_response_with(mock_request, dangal_movie)
        self.movie_client_mock_server.not_found_response(mock_request, "Wanted")

        response = self.test_client.post("/movies-snapshots",
                                         json={"titles": ['Dangal', 'Wanted']},
                                         headers=authorization_header())

        expected_json = [
            {
                'director': 'Rajkumar Hirani',
                'ratings': [
                    {'source': 'Internet Movie Database', 'value': '8.4/10'},
                    {'source': 'Rotten Tomatoes', 'value': '100%'}],
                'releaseDate': '25 Dec 2009',
                'releaseYear': '2009',
                'title': 'Dangal',
                'id': mock.ANY,
                'is_empty': False
            },
            {
                'is_empty': True,
                'title': 'Wanted'
            }
        ]

        self.assertEqual(expected_json, response.get_json())
        self.assertEqual(201, response.status_code)

        saved_movie_snapshots = MovieSnapshotFixture.find_all()
        self.assertEqual(1, len(saved_movie_snapshots))

        saved_movie = saved_movie_snapshots[0]
        self.assertEqual('Dangal', saved_movie.title)

    def test_should_get_all_movie_snapshots(self):
        ratings = RatingEntity(source='Internet Movie Database', value='8.4/10')
        movie_snapshot = MovieSnapshotEntity(title="3 Idiots",
                                             release_year="2009",
                                             release_date='25 Dec 2009',
                                             director='Rajkumar Hirani',
                                             ratings=[ratings])

        MovieSnapshotFixture.save(movie_snapshot)

        response = self.test_client.get("/movies-snapshots")

        expected_json = [
            {
                'director': 'Rajkumar Hirani',
                'ratings': [{'source': 'Internet Movie Database', 'value': '8.4/10'}],
                'releaseDate': '25 Dec 2009',
                'releaseYear': '2009',
                'title': '3 Idiots',
                'id': mock.ANY,
                'is_empty': False
            }
        ]
        self.assertEqual(200, response.status_code)
        self.assertEqual(expected_json, response.get_json())
