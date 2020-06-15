import unittest
from unittest.mock import patch

from mmasters.app import Application
from tests.builder.movie_snapshot_view_builder import MovieSnapshotViewBuilder
from tests.config.test_config import TestConfig


def authorization_header():
    return {'x-api-key': TestConfig.API_KEY}


class MovieSnapshotResourceTest(unittest.TestCase):

    def setUp(self):
        self.app = Application.create_app(TestConfig)
        self.test_client = self.app.test_client()
        self.movie_snapshot_service_patch = patch("mmasters.resource.movie_snapshot_resource.movie_snapshot_service")
        self.movie_snapshot_service = self.movie_snapshot_service_patch.start()

    def tearDown(self) -> None:
        self.movie_snapshot_service_patch.stop()

    def test_should_return_status_code_as_created_when_movies_snapshots_are_created(self):
        response = self.test_client.post("/movies-snapshots",
                                         json={"titles": ['3 Idiots', 'Dangal']},
                                         headers=authorization_header())

        self.assertEqual(201, response.status_code)

    def test_should_return_created_movie_snapshots(self):
        self.movie_snapshot_service.create.return_value = [MovieSnapshotViewBuilder().with_title("3 Idiots").build()]

        response = self.test_client.post("/movies-snapshots",
                                         json={"titles": ['3 Idiots']},
                                         headers=authorization_header())

        expected_json = [{'director': 'Timur Bekmambetov',
                          'ratings': [{'source': 'Internet Movie Database', 'value': '6.7/10'},
                                      {'source': 'Rotten Tomatoes', 'value': '71%'}],
                          'releaseDate': '27 June 2008',
                          'releaseYear': '2008',
                          'title': '3 Idiots',
                          'is_empty': False
                          }]
        self.assertEqual(expected_json, response.get_json())

    def test_should_create_movie_snapshots_with_titles_passed_as_payload(self):
        self.movie_snapshot_service.create.return_value = [MovieSnapshotViewBuilder().with_title("3 Idiots").build()]

        self.test_client.post("/movies-snapshots",
                              json={"titles": ['3 Idiots']},
                              headers=authorization_header())

        self.movie_snapshot_service.create.assert_called_with(['3 Idiots'])

    def test_should_return_bad_request_as_status_when_titles_is_missing_in_payload(self):
        self.movie_snapshot_service.create.return_value = [MovieSnapshotViewBuilder().with_title("3 Idiots").build()]

        response = self.test_client.post("/movies-snapshots",
                                         json={},
                                         headers=authorization_header())

        self.assertEqual(400, response.status_code)

    def test_should_return_bad_request_as_status_when_titles_is_empty_list_in_payload(self):
        self.movie_snapshot_service.create.return_value = [MovieSnapshotViewBuilder().with_title("3 Idiots").build()]

        response = self.test_client.post("/movies-snapshots",
                                         json={'titles': []},
                                         headers=authorization_header())

        self.assertEqual(400, response.status_code)

    def test_should_return_error_message_in_response_when_titles_is_missing_in_payload(self):
        self.movie_snapshot_service.create.return_value = [MovieSnapshotViewBuilder().with_title("3 Idiots").build()]

        response = self.test_client.post("/movies-snapshots",
                                         json={},
                                         headers=authorization_header())

        expected_message = {'message': {'titles': 'titles is a mandatory field'}}
        self.assertEqual(expected_message, response.get_json())

    def test_should_return_unauthorized_as_status_code_when_api_key_is_missing_in_header(self):
        response = self.test_client.post("/movies-snapshots", json={"titles": ['3 Idiots']})

        self.assertEqual(401, response.status_code)

    def test_should_return_status_code_as_200_for_get_request_for_movie_snapshots(self):
        self.movie_snapshot_service.get_all.return_value = [MovieSnapshotViewBuilder().with_title("3 Idiots").build()]

        response = self.test_client.get("/movies-snapshots")

        self.assertEqual(200, response.status_code)

    def test_should_return_movie_snapshots_in_response_body_for_get_request_for_movie_snapshots(self):
        self.movie_snapshot_service.get_all.return_value = [MovieSnapshotViewBuilder().with_title("3 Idiots").build()]

        response = self.test_client.get("/movies-snapshots")

        expected_json = [{"director": "Timur Bekmambetov",
                          "ratings": [{"source": "Internet Movie Database", "value": "6.7/10"},
                                      {"source": "Rotten Tomatoes", "value": "71%"}],
                          "releaseDate": "27 June 2008",
                          "releaseYear": "2008",
                          "title": "3 Idiots",
                          'is_empty': False}]

        self.assertEqual(expected_json, response.get_json())

    def test_should_retrieve_movie_snapshots_from_movie_snapshot_service(self):
        self.movie_snapshot_service.get_all.return_value = [MovieSnapshotViewBuilder().with_title("3 Idiots").build()]

        self.test_client.get("/movies-snapshots")

        self.movie_snapshot_service.get_all.assert_called_once()
