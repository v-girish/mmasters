from http import HTTPStatus

from flask_restful import Resource, marshal_with, reqparse

from mmasters.service.movie_snapshot_service import movie_snapshot_service
from mmasters.view.movie_snapshot_view import movie_snapshot_view_fields


class MovieSnapshotResource(Resource):

    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('titles', action='append', required=True, help="titles is a mandatory field")

    @marshal_with(fields=movie_snapshot_view_fields)
    def post(self):
        args = self.parser.parse_args()
        movie_snapshots = movie_snapshot_service.create(args["titles"])
        return movie_snapshots, HTTPStatus.CREATED
