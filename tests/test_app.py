from unittest import TestCase

from mmasters.app import Application


class TestApplication(TestCase):

    def test_should_create_a_flask_app(self):
        app = Application.create_app()
        self.assertFalse(None, app)
