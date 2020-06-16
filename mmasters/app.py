from typing import Type

from flask import Flask
from flask_migrate import Migrate

from mmasters.config.config import Config
from mmasters.config.database import db
from mmasters.config.endpoints import Endpoints
from mmasters.config.logging_config import setup_logging


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
        Endpoints(app).add()

    @staticmethod
    def setup_database(app):
        db.init_app(app)
        Migrate(app, db)
