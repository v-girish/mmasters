from unittest import TestCase

from mmasters.app import Application
from tests.config.test_config import TestConfig


class TestApplication(TestCase):

    def test_should_create_a_flask_app(self):
        app = Application.create_app(TestConfig)
        self.assertFalse(None, app)
