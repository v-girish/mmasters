import unittest

from flask import Flask

from mmasters.config.endpoints import Endpoints


class EndpointsTest(unittest.TestCase):

    def setUp(self):
        self.app = Flask(__name__)

    def test_should_add_movie_snapshot_endpoint(self):
        endpoints = Endpoints(app=self.app)

        endpoints.add()

        self.assertEqual(1, len(endpoints.api.endpoints))
        self.assertEqual('moviesnapshotresource', list(endpoints.api.endpoints)[0])
