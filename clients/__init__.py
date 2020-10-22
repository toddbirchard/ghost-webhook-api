"""Initialize clients and third-party services."""
from google.cloud import bigquery as bigquery_client

from clients.database import Database
from clients.ghost import Ghost
from clients.sms import Twilio
from clients.storage import GCS
from config import Config

# Database connection
db = Database(uri=Config.SQLALCHEMY_DATABASE_URI, args=Config.SQLALCHEMY_ENGINE_OPTIONS)

# Google Cloud Storage
gcs = GCS(
    bucket_name=Config.GCP_BUCKET_NAME,
    bucket_url=Config.GCP_BUCKET_URL,
    bucket_lynx=Config.GCP_LYNX_DIRECTORY,
)

# Ghost Admin Client
ghost = Ghost(
    api_url=Config.GHOST_ADMIN_API_URL,
    client_id=Config.GHOST_CLIENT_ID,
    client_secret=Config.GHOST_ADMIN_API_KEY,
    netlify_build_url=Config.GHOST_NETLIFY_BUILD_HOOK,
)

# Twilio SMS
sms = Twilio(
    sid=Config.TWILIO_ACCOUNT_SID,
    token=Config.TWILIO_AUTH_TOKEN,
    recipient=Config.TWILIO_RECIPIENT_PHONE,
    sender=Config.TWILIO_SENDER_PHONE,
)

# Google BigQuery
bigquery = bigquery_client.Client()
