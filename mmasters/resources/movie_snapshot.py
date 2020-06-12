from functools import wraps
from http import HTTPStatus

import flask_restful
from flask import request
from flask_restful import Resource, marshal_with, reqparse

from mmasters.service.movie_snapshot_service import movie_snapshot_service
from mmasters.view.movie_snapshot_view import movie_snapshot_view_fields


def api_key_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        api_key = request.headers.get('x-api-key')
        if api_key != 'abc':
            flask_restful.abort(HTTPStatus.UNAUTHORIZED)
        return func(*args, **kwargs)

    return wrapper


class MovieSnapshotResource(Resource):

    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('titles', action='append', required=True, help="titles is a mandatory field")

    @marshal_with(fields=movie_snapshot_view_fields)
    @api_key_required
    def post(self):
        args = self.parser.parse_args()
        movie_snapshots = movie_snapshot_service.create(args["titles"])
        return movie_snapshots, HTTPStatus.CREATED
