from http import HTTPStatus
from unittest import TestCase, mock
from unittest.mock import Mock

from werkzeug.exceptions import Unauthorized

from mmasters.decorator.api_key_authentication import api_key_required


class Test(TestCase):

    def test_should_raise_unauthorized_exception_when_api_key_is_missing_in_request_header(self):
        request = mock.MagicMock()
        request.headers = {}

        app = mock.MagicMock()
        app.config = {'API_KEY': 'api_key'}

        with mock.patch("mmasters.decorator.api_key_authentication.request", request):
            with mock.patch("mmasters.decorator.api_key_authentication.app", app):
                wrapper_func = api_key_required(Mock())
                self.assertRaises(Unauthorized, wrapper_func)

    def test_should_raise_unauthorized_exception_with_message_when_api_key_is_missing_in_request_header(self):
        request = mock.MagicMock()
        request.headers = {'x-api-key': 'incorrect-api-key'}

        app = mock.MagicMock()
        app.config = {'API_KEY': 'api_key'}

        with mock.patch("mmasters.decorator.api_key_authentication.request", request):
            with mock.patch("mmasters.decorator.api_key_authentication.app", app):
                with self.assertRaises(Unauthorized) as context:
                    api_key_required(Mock())()
                self.assertEqual('Incorrect API KEY', context.exception.data['message'])

    def test_should_invoke_function_given_authorized_request(self):
        request = mock.MagicMock()
        request.headers = {"x-api-key": 'api_key'}

        app = mock.MagicMock()
        app.config = {'API_KEY': 'api_key'}

        with mock.patch("mmasters.decorator.api_key_authentication.request", request):
            with mock.patch("mmasters.decorator.api_key_authentication.app", app):
                mock_function = Mock()

                api_key_required(mock_function)()

                mock_function.assert_called_once()
