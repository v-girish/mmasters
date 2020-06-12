from http import HTTPStatus

from flask import Response
from flask_restful import Resource


class MovieSnapshotResource(Resource):

    def post(self) -> Response:
        return Response("", status=HTTPStatus.CREATED)
