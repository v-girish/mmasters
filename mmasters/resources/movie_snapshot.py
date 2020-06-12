from http import HTTPStatus

from flask_restful import Resource, marshal_with

from mmasters.service.movie_snapshot_service import movie_snapshot_service
from mmasters.view.movie_snapshot_view import movie_snapshot_view_fields


class MovieSnapshotResource(Resource):

    @marshal_with(fields=movie_snapshot_view_fields)
    def post(self):
        movie_snapshots = movie_snapshot_service.create()
        return movie_snapshots, HTTPStatus.CREATED
