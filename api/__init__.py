"""Initialize api."""
from flask import Flask
from api.database import Database
from api.gcs import GCS
from config import Config

db = Database(Config.SQLALCHEMY_DATABASE_URI, Config.SQLALCHEMY_ENGINE_OPTIONS)
gcs = GCS(Config.GCP_BUCKET_NAME)


def init_api():
    """Construct the core application."""
    api = Flask(__name__, instance_relative_config=False)

    # Application Configuration
    api.config.from_object('config.Config')

    with api.app_context():
        # Import parts of our api
        from api.metadata import routes
        from api.images import routes
        from api.lynx import routes
        from api.algolia import routes

        return api
