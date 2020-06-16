from typing import Type

from flask import Flask
from flask_migrate import Migrate
from flask_restful import Api

from mmasters.config.config import Config
from mmasters.config.db_config import db
from mmasters.config.logging_config import setup_logging
from mmasters.resource.movie_snapshot_resource import MovieSnapshotResource


class Application:

    @staticmethod
    def create_app(config: Type[Config]) -> Flask:
        setup_logging()

        app = Application.initialize_app()

        Application.configure(app, config)

        Application.add_resources(app)

        Application.setup_database(app)

        return app

    @staticmethod
    def initialize_app():
        return Flask(__name__)

    @staticmethod
    def configure(app, config):
        app.config.from_object(config)

    @staticmethod
    def add_resources(app):
        api = Api(app)
        api.add_resource(MovieSnapshotResource, '/movies-snapshots')

    @staticmethod
    def setup_database(app):
        db.init_app(app)
        Migrate(app, db)
