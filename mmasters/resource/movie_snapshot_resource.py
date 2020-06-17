import logging
from http import HTTPStatus

from flask_restful import Resource, marshal_with, reqparse

from mmasters.decorator.api_key_authentication import api_key_required
from mmasters.model.movie_snapshot_creation_response import MovieSnapshotCreationResponse
from mmasters.service.movie_snapshot_service import movie_snapshot_service
from mmasters.view.movie_snapshot_view import MovieSnapshotView


class MovieSnapshotResource(Resource):

    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('titles', action='append', required=True, help="titles is a mandatory field")
        self.logger = logging.getLogger(__name__)

    @api_key_required
    @marshal_with(MovieSnapshotCreationResponse.json_fields)
    def post(self):
        args = self.parser.parse_args()
        titles = args['titles']
        self.logger.debug(f"Creating movie snapshots for titles {titles}")

        movie_creation_response = movie_snapshot_service.create(titles)

        return movie_creation_response, HTTPStatus.CREATED

    @marshal_with(fields=MovieSnapshotView.json_fields)
    def get(self):
        movie_snapshots = movie_snapshot_service.get_all()
        return movie_snapshots, HTTPStatus.OK
