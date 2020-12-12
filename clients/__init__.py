"""Initialize clients and third-party services."""
from google.cloud import bigquery as bigquery_client

from clients.ghost import Ghost
from clients.mail import Mailgun
from clients.sms import Twilio
from clients.storage import GCS
from config import Settings

# Google Cloud Storage
gcs = GCS(
    bucket_name=Settings().GCP_BUCKET_NAME,
    bucket_url=Settings().GCP_BUCKET_URL,
    bucket_lynx=Settings().GCP_LYNX_DIRECTORY,
)

# Ghost Admin Client
ghost = Ghost(
    admin_api_url=Settings().GHOST_ADMIN_API_URL,
    content_api_url=Settings().GHOST_CONTENT_API_URL,
    client_id=Settings().GHOST_CLIENT_ID,
    client_secret=Settings().GHOST_ADMIN_API_KEY,
    netlify_build_url=Settings().GHOST_NETLIFY_BUILD_HOOK,
)

# Twilio SMS
sms = Twilio(
    sid=Settings().TWILIO_ACCOUNT_SID,
    token=Settings().TWILIO_AUTH_TOKEN,
    recipient=Settings().TWILIO_RECIPIENT_PHONE,
    sender=Settings().TWILIO_SENDER_PHONE,
)

# Google BigQuery
bigquery = bigquery_client.Client()

# Mailgun SMTP
mailgun = Mailgun(
    Settings().MAILGUN_EMAIL_SERVER,
    Settings().MAILGUN_FROM_SENDER,
    Settings().MAILGUN_API_KEY,
)
