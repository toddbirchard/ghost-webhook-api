"""Initialize clients and third-party SDKs."""

from github import Github
from google.cloud import bigquery

from clients.ghost import Ghost
from clients.img import ImageTransformer
from clients.mail import Mailgun
from clients.sms import Twilio
from config import settings

# Google Cloud Storage
images = ImageTransformer(
    gcp_project_name=settings.GOOGLE_CLOUD_PROJECT_NAME,
    gcp_api_credentials=settings.GOOGLE_CLOUD_CREDENTIALS,
    bucket_name=settings.GCP_BUCKET_NAME,
    bucket_url=settings.GCP_BUCKET_URL,
)

# Ghost Admin Client
ghost = Ghost(
    admin_api_url=settings.GHOST_ADMIN_API_URL,
    api_version=settings.GHOST_API_VERSION,
    content_api_url=settings.GHOST_CONTENT_API_URL,
    client_id=settings.GHOST_CLIENT_ID,
    client_secret=settings.GHOST_ADMIN_API_KEY,
    content_api_key=settings.GHOST_CONTENT_API_KEY,
)

# Twilio SMS
sms = Twilio(
    sid=settings.TWILIO_ACCOUNT_SID,
    token=settings.TWILIO_AUTH_TOKEN,
    recipient=settings.TWILIO_RECIPIENT_PHONE,
    sender=settings.TWILIO_SENDER_PHONE,
)

# Google BigQuery
gbq = bigquery.Client(
    project=settings.GOOGLE_CLOUD_PROJECT_NAME,
    credentials=settings.GOOGLE_CLOUD_CREDENTIALS,
)

# Mailgun SMTP
mailgun = Mailgun(
    settings.MAILGUN_EMAIL_SERVER,
    settings.MAILGUN_FROM_SENDER_EMAIL,
    settings.MAILGUN_SENDER_API_KEY,
)

# Github
gh = Github(settings.GITHUB_API_KEY)
