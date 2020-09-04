"""Clients and services."""
from clients.database import Database
from clients.storage import GCS
from clients.ghost import Ghost
from clients.sms import Twilio
from config import Config
from google.cloud import bigquery as bigquery_client


# Initialize clients
db = Database(
    uri=Config.SQLALCHEMY_DATABASE_URI,
    args=Config.SQLALCHEMY_ENGINE_OPTIONS
)
gcs = GCS(
    bucket_name=Config.GCP_BUCKET_NAME,
    bucket_url=Config.GCP_BUCKET_URL,
    bucket_lynx=Config.GCP_LYNX_DIRECTORY
)
ghost = Ghost(
    api_url=Config.GHOST_ADMIN_API_URL,
    client_id=Config.GHOST_CLIENT_ID,
    client_secret=Config.GHOST_ADMIN_API_KEY,
 )
sms = Twilio(
    sid=Config.TWILIO_ACCOUNT_SID,
    token=Config.TWILIO_AUTH_TOKEN,
    recipient=Config.TWILIO_RECIPIENT_PHONE,
    sender=Config.TWILIO_SENDER_PHONE
)
bigquery = bigquery_client.Client()
