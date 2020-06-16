from flask_restful import Api

from mmasters.resource.movie_snapshot_resource import MovieSnapshotResource


class Endpoints:

    def __init__(self, app):
        self.api = Api(app)

    def add(self):
        self.api.add_resource(MovieSnapshotResource, '/movies-snapshots')