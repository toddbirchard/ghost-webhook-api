"""Initialize api."""
from flask import Flask
from api.database import Database
from api.gcs import GCS
from api.bigquery import BigQuery
from api.ghost import Ghost
from api.sms import Twilio
from api.transform import ImageTransformer
from config import Config

# Initialize clients
db = Database(Config.SQLALCHEMY_DATABASE_URI, Config.SQLALCHEMY_ENGINE_OPTIONS)
gcs = GCS(Config.GCP_BUCKET_NAME, Config.GCP_BUCKET_URL, Config.GCP_LYNX_DIRECTORY)
gbq = BigQuery(Config.GCP_BIGQUERY_URI)
ghost = Ghost(Config.GHOST_API_KEY, Config.GHOST_API_BASE_URL)
sms = Twilio(Config)
image = ImageTransformer(gcs)


def init_api():
    """Construct the core application."""
    api = Flask(__name__, instance_relative_config=False)
    api.config.from_object('config.Config')

    with api.app_context():
        from api import (
            posts,
            images,
            algolia,
            analytics,
            members,
            authors,
            donate
        )

        return api
