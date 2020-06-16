from mmasters.config.config import Config


class TestConfig(Config):
    API_KEY = "api_key"
    OMDB_API_KEY = "omdb_api_key"
    OMDB_API_BASE_URL = "http://localhost:9999"
    SQLALCHEMY_DATABASE_URI = "postgresql://postgres:secret@localhost:5432/mmasters"

