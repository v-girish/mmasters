import unittest

from flask import Flask
from flask_restful import Api

from mmasters.resources.greetings import GreetingsResource


class GreetingsResourceTest(unittest.TestCase):

    def setUp(self):
        self.app = Flask(__name__)
        api = Api(self.app)
        api.add_resource(GreetingsResource, '/greetings')
        self.test_client = self.app.test_client()

    def test_should_return_greetings(self):
        response = self.test_client.get("/greetings")
        self.assertEqual("Hello World", response.get_json())
