from flask import Flask
from flask_restful import Api

from mmasters.resources.greetings import GreetingsResource
from mmasters.resources.movie_snapshot import MovieSnapshotResource


class Application:

    @staticmethod
    def create_app() -> Flask:
        app = Flask(__name__)
        api = Api(app)

        api.add_resource(GreetingsResource, '/greetings')
        api.add_resource(MovieSnapshotResource, '/movies-snapshots')

        return app
