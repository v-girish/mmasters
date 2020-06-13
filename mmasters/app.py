from typing import Type

from flask import Flask
from flask_migrate import Migrate
from flask_restful import Api

from mmasters.config.config import Config
from mmasters.config.db_config import db
from mmasters.resource.movie_snapshot_resource import MovieSnapshotResource


class Application:

    @staticmethod
    def create_app(config: Type[Config]) -> Flask:
        app = Flask(__name__)
        app.config.from_object(config)

        api = Api(app)

        api.add_resource(MovieSnapshotResource, '/movies-snapshots')

        db.init_app(app)
        Migrate(app, db)

        return app
