import unittest
from unittest.mock import patch

from mmasters.app import Application
from mmasters.view.movie_snapshot_view import MovieSnapshotView
from tests.config.test_config import TestConfig


def authorization_header():
    return {'x-api-key': TestConfig.API_KEY}


class MovieSnapshotResourceTest(unittest.TestCase):

    def setUp(self):
        self.app = Application.create_app(TestConfig)
        self.test_client = self.app.test_client()
        self.movie_snapshot_service_patch = patch("mmasters.resources.movie_snapshot_resource.movie_snapshot_service")
        self.movie_snapshot_service = self.movie_snapshot_service_patch.start()

    def tearDown(self) -> None:
        self.movie_snapshot_service_patch.stop()

    def test_should_return_status_code_as_created_when_movies_snapshots_are_created(self):
        response = self.test_client.post("/movies-snapshots",
                                         json={"titles": ['3 Idiots', 'Dangal']},
                                         headers=authorization_header())

        self.assertEqual(201, response.status_code)

    def test_should_return_created_movie_snapshots(self):
        self.movie_snapshot_service.create.return_value = [MovieSnapshotView('3 Idiots', "2009")]

        response = self.test_client.post("/movies-snapshots",
                                         json={"titles": ['3 Idiots']},
                                         headers=authorization_header())

        expected_json = [{
            "title": "3 Idiots",
            "releaseYear": "2009"
        }]
        self.assertEqual(expected_json, response.get_json())

    def test_should_create_movie_snapshots_with_titles_passed_as_payload(self):
        self.movie_snapshot_service.create.return_value = [MovieSnapshotView('3 Idiots', "2009")]

        self.test_client.post("/movies-snapshots",
                              json={"titles": ['3 Idiots']},
                              headers=authorization_header())

        self.movie_snapshot_service.create.assert_called_with(['3 Idiots'])

    def test_should_return_bad_request_as_status_when_titles_is_missing_in_payload(self):
        self.movie_snapshot_service.create.return_value = [MovieSnapshotView('3 Idiots', "2009")]

        response = self.test_client.post("/movies-snapshots",
                                         json={},
                                         headers=authorization_header())

        self.assertEqual(400, response.status_code)

    def test_should_return_bad_request_as_status_when_titles_is_empty_list_in_payload(self):
        self.movie_snapshot_service.create.return_value = [MovieSnapshotView('3 Idiots', "2009")]

        response = self.test_client.post("/movies-snapshots",
                                         json={'titles': []},
                                         headers=authorization_header())

        self.assertEqual(400, response.status_code)

    def test_should_return_error_message_in_response_when_titles_is_missing_in_payload(self):
        self.movie_snapshot_service.create.return_value = [MovieSnapshotView('3 Idiots', "2009")]

        response = self.test_client.post("/movies-snapshots",
                                         json={},
                                         headers=authorization_header())

        expected_message = {'message': {'titles': 'titles is a mandatory field'}}
        self.assertEqual(expected_message, response.get_json())

    def test_should_return_unauthorized_as_status_code_when_api_key_is_missing_in_header(self):
        response = self.test_client.post("/movies-snapshots", json={"titles": ['3 Idiots']})

        self.assertEqual(401, response.status_code)

