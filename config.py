"""Flask API configuration."""
import datetime
from os import getenv, path

from dotenv import load_dotenv
from pydantic import BaseSettings

# Load variables from .env
basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, ".env"))


class Settings(BaseSettings):
    app_name: str = "Jamstack API"
    title: str = "Jamstack API"
    description: str = "API to automate optimizations for JAMStack sites."
    items_per_user: int = 50
    debug: bool = True

    # General Config
    secret_key = getenv("SECRET_KEY")
    environment: str = getenv("ENVIRONMENT")
    dt: datetime.datetime = datetime.datetime.today()
    cors_origins = [
        "http://hackersandslackers.com",
        "https://hackersandslackers.app",
        "http://localhost",
        "http://localhost:8080",
    ]
    openapi_tags = (
        [
            {
                "name": "posts",
                "description": "Sanitation and optimization of post data.",
            },
            {
                "name": "accounts",
                "description": "User account signup and actions.",
            },
            {
                "name": "authors",
                "description": "New author management.",
            },
            {
                "name": "newsletter",
                "description": "Ghost newsletter subscription management.",
            },
            {
                "name": "analytics",
                "description": "Fetch site traffic & search query analytics.",
            },
        ],
    )

    env_file = ".env"

    # Database
    SQLALCHEMY_DATABASE_URI = getenv("SQLALCHEMY_DATABASE_URI")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {"ssl": {"ca": "./creds/ca-certificate.crt"}}

    # Algolia API
    ALGOLIA_BASE_URL = getenv("ALGOLIA_BASE_URL")
    ALGOLIA_APP_ID = getenv("ALGOLIA_APP_ID")
    ALGOLIA_API_KEY = getenv("ALGOLIA_API_KEY")

    # Google Cloud storage
    GCP_BUCKET_URL = getenv("GCP_BUCKET_URL")
    GCP_BUCKET_NAME = getenv("GCP_BUCKET_NAME")
    GOOGLE_APPLICATION_CREDENTIALS = path.join(basedir, "gcloud.json")
    GCP_BUCKET_FOLDER = [f'{dt.year}/{dt.strftime("%m")}']
    GCP_LYNX_DIRECTORY = "roundup"

    # Google BigQuery
    GCP_PROJECT = getenv("GCP_PROJECT")
    GCP_BIGQUERY_TABLE = getenv("GCP_BIGQUERY_TABLE")
    GCP_BIGQUERY_DATASET = getenv("GCP_BIGQUERY_DATASET")
    GCP_BIGQUERY_URI = f"bigquery://{GCP_PROJECT}/{GCP_BIGQUERY_DATASET}"

    # Ghost
    GHOST_BASE_URL = getenv("GHOST_BASE_URL")
    GHOST_ADMIN_API_URL = f"{GHOST_BASE_URL}/ghost/api/v3/admin"
    GHOST_CONTENT_API_URL = f"{GHOST_BASE_URL}/ghost/api/v3/"
    GHOST_API_USERNAME = getenv("GHOST_API_USERNAME")
    GHOST_API_PASSWORD = getenv("GHOST_API_PASSWORD")
    GHOST_CLIENT_ID = getenv("GHOST_CLIENT_ID")
    GHOST_ADMIN_API_KEY = getenv("GHOST_ADMIN_API_KEY")
    GHOST_API_EXPORT_URL = f"{GHOST_BASE_URL}/admin/db/"
    GHOST_NETLIFY_BUILD_HOOK = getenv("GHOST_NETLIFY_BUILD_HOOK")

    # Mailgun
    MAILGUN_EMAIL_SERVER = getenv("MAILGUN_EMAIL_SERVER")
    MAILGUN_EMAIL_TEMPLATE = getenv("MAILGUN_EMAIL_TEMPLATE")
    MAILGUN_API_KEY = getenv("MAILGUN_API_KEY")
    MAILGUN_FROM_SENDER = getenv("MAILGUN_FROM_SENDER")
    MAILGUN_SUBJECT_LINE = "To Hack or to Slack; That is the Question."
    MAILGUN_PERSONAL_EMAIL = getenv("MAILGUN_PERSONAL_EMAIL")

    # Mixpanel
    MIXPANEL_API_TOKEN = getenv("MIXPANEL_API_TOKEN")

    # Twilio
    TWILIO_SENDER_PHONE = getenv("TWILIO_SENDER_PHONE")
    TWILIO_RECIPIENT_PHONE = getenv("TWILIO_RECIPIENT_PHONE")
    TWILIO_AUTH_TOKEN = getenv("TWILIO_AUTH_TOKEN")
    TWILIO_ACCOUNT_SID = getenv("TWILIO_ACCOUNT_SID")

    # Datadog
    DATADOG_API_KEY: str = getenv("DATADOG_API_KEY")
    DATADOG_APP_KEY: str = getenv("DATADOG_APP_KEY")
    dd_trace: bool = getenv("DATADOG_TRACE_ENABLED")
