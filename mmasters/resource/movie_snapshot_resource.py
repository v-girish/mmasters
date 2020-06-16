import logging
from http import HTTPStatus

from flask_restful import Resource, marshal_with, reqparse

from mmasters.decorator.api_key_authentication import api_key_required
from mmasters.service.movie_snapshot_service import movie_snapshot_service
from mmasters.view.movie_snapshot_view import MovieSnapshotView


class MovieSnapshotResource(Resource):

    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('titles', action='append', required=True, help="titles is a mandatory field")
        self.logger = logging.getLogger(__name__)

    @api_key_required
    def post(self):
        args = self.parser.parse_args()
        self.logger.debug(f"Creating movie snapshots for titles {args['titles']}")

        movie_snapshot_views = movie_snapshot_service.create(args["titles"])

        movie_snapshots = [movie_snapshot_view.marshal() for movie_snapshot_view in movie_snapshot_views]

        return movie_snapshots, HTTPStatus.CREATED

    @marshal_with(fields=MovieSnapshotView.json_fields)
    def get(self):
        movie_snapshots = movie_snapshot_service.get_all()
        return movie_snapshots, HTTPStatus.OK
