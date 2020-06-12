import unittest
from unittest.mock import patch

from mmasters.app import Application
from mmasters.service.movie_snapshot_service import MovieSnapshotService
from mmasters.view.movie_snapshot_view import MovieSnapshotView


class MovieSnapshotResourceTest(unittest.TestCase):

    def setUp(self):
        self.app = Application.create_app()
        self.test_client = self.app.test_client()

    @patch("mmasters.resources.movie_snapshot.movie_snapshot_service")
    def test_should_return_status_code_as_created_when_movies_snapshots_are_created(self, movie_snapshot_service: MovieSnapshotService):
        response = self.test_client.post("/movies-snapshots", data={"titles": ['3 Idiots', 'Dangal']})

        self.assertEqual(201, response.status_code)

    @patch("mmasters.resources.movie_snapshot.movie_snapshot_service")
    def test_should_return_created_movie_snapshots(self, movie_snapshot_service: MovieSnapshotService):
        movie_snapshot_service.create.return_value = [MovieSnapshotView('3 Idiots', "2009")]

        response = self.test_client.post("/movies-snapshots", data={"titles": ['3 Idiots']})

        expected_json = [{
            "title": "3 Idiots",
            "releaseYear": "2009"
        }]
        self.assertEqual(expected_json, response.get_json())

    @patch("mmasters.resources.movie_snapshot.movie_snapshot_service")
    def test_should_create_movie_snapshots_with_titles_passed_as_payload(self, movie_snapshot_service: MovieSnapshotService):
        movie_snapshot_service.create.return_value = [MovieSnapshotView('3 Idiots', "2009")]

        self.test_client.post("/movies-snapshots", json={"titles": ['3 Idiots']})

        movie_snapshot_service.create.assert_called_with(['3 Idiots'])
