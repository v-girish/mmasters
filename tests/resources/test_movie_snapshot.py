import unittest

from mmasters.app import Application


class MovieSnapshotResourceTest(unittest.TestCase):

    def setUp(self):
        self.app = Application.create_app()
        self.test_client = self.app.test_client()

    def test_should_return_status_code_as_created_when_movies_snapshots_are_created(self):
        response = self.test_client.post("/movies-snapshots", data={"titles": ['3 Idiots', 'Dangal']})

        self.assertEqual(201, response.status_code)
