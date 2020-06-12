from functools import wraps
from http import HTTPStatus

import flask_restful
from flask import request, current_app as app, Response


def api_key_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        api_key = request.headers.get('x-api-key')
        if api_key != app.config.get('API_KEY'):
            return flask_restful.abort(HTTPStatus.UNAUTHORIZED, message='Incorrect API KEY')
        return func(*args, **kwargs)

    return wrapper
