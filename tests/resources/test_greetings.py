import unittest

from mmasters.app import Application
from tests.config.test_config import TestConfig


class GreetingsResourceTest(unittest.TestCase):

    def setUp(self):
        self.app = Application.create_app(TestConfig)
        self.test_client = self.app.test_client()

    def test_should_return_greetings(self):
        response = self.test_client.get("/greetings")
        self.assertEqual("Hello World", response.get_json())
