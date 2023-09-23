"""FastAPI configuration."""
from datetime import datetime
from os import getenv, path
from os.path import exists
from typing import ClassVar, List

from dotenv import load_dotenv
from fastapi_mail import ConnectionConfig
from google.oauth2 import service_account
from google.oauth2.service_account import Credentials
from pydantic import EmailStr
from pydantic_settings import BaseSettings, SettingsConfigDict

# Set relative directory path for project root.
BASE_DIR = path.abspath(path.dirname(__file__))
load_dotenv(path.join(BASE_DIR, ".env"))


class Settings(BaseSettings):
    """FastAPI settings & configuration."""

    model_config = SettingsConfigDict(env_file=".env")

    app_name: str = "Blog Webhook API"
    title: str = "Blog Webhook API"
    description: str = "API to automate optimizations for blog sites."
    items_per_user: int = 50
    debug: bool = True

    # General Config
    SECRET_KEY: str = getenv("SECRET_KEY")
    ENVIRONMENT: str = getenv("ENVIRONMENT")
    CORS_ORIGINS: list = [
        "http://hackersandslackers.com",
        "http://localhost",
        "http://localhost:8080",
        "http://api.hackersandslackers.com",
        "https://api.hackersandslackers.com",
        "http://zapier.com",
        "https://zapier.com",
        "https://zapier.com/",
        "https://zapier.com/*",
        "*",
    ]

    API_TAGS: List[dict] = (
        [
            {
                "name": "posts",
                "description": "Sanitation and optimization of post metadata.",
            },
            {
                "name": "accounts",
                "description": "User account signup and actions.",
            },
            {
                "name": "authors",
                "description": "Author management.",
            },
            {
                "name": "newsletter",
                "description": "Ghost newsletter subscriptions.",
            },
            {
                "name": "analytics",
                "description": "Migrate site traffic & search query analytics.",
            },
            {
                "name": "images",
                "description": "Image optimization for retina and mobile devices.",
            },
            {
                "name": "github",
                "description": "Github notifications for new issues/PRs.",
            },
        ],
    )

    # Date
    TODAY_DATE: datetime = datetime.today()

    # Database
    SQLALCHEMY_DATABASE_URI: str = getenv("SQLALCHEMY_DATABASE_URI")
    SQLALCHEMY_GHOST_DATABASE_NAME: str = getenv("SQLALCHEMY_GHOST_DATABASE_NAME")
    SQLALCHEMY_FEATURES_DATABASE_NAME: str = getenv("SQLALCHEMY_FEATURES_DATABASE_NAME")
    SQLALCHEMY_DATABASE_PEM: str = getenv("SQLALCHEMY_DATABASE_PEM")
    SQLALCHEMY_TRACK_MODIFICATIONS: bool = False
    SQLALCHEMY_ENGINE_OPTIONS: dict = {"ssl": {"key": SQLALCHEMY_DATABASE_PEM}}

    # Algolia API
    ALGOLIA_SEARCHES_ENDPOINT: str = "https://analytics.algolia.com/2/searches"
    ALGOLIA_APP_ID: str = getenv("ALGOLIA_APP_ID")
    ALGOLIA_API_KEY: str = getenv("ALGOLIA_API_KEY")
    ALGOLIA_TABLE_WEEKLY: str = "algolia_searches_week"
    ALGOLIA_TABLE_MONTHLY: str = "algolia_searches_month"

    # Google Cloud Auth
    GOOGLE_CREDENTIALS: str = getenv("GOOGLE_CREDENTIALS")
    GOOGLE_CLOUD_PROJECT_NAME: str = getenv("GOOGLE_CLOUD_PROJECT_NAME")
    GOOGLE_CLOUD_JSON_FILEPATH: str = getenv("GOOGLE_CLOUD_JSON_FILEPATH")
    GOOGLE_CLOUD_CREDENTIALS: Credentials
    if exists(f"{BASE_DIR}/{GOOGLE_CLOUD_JSON_FILEPATH}"):
        GOOGLE_CLOUD_CREDENTIALS: Credentials = service_account.Credentials.from_service_account_file(
            f"{BASE_DIR}/{GOOGLE_CLOUD_JSON_FILEPATH}"
        )
    else:
        GOOGLE_CLOUD_CREDENTIALS = GOOGLE_CREDENTIALS

    # Google BigQuery
    GCP_BIGQUERY_TABLE: str = getenv("GCP_BIGQUERY_TABLE")
    GCP_BIGQUERY_DATASET: str = getenv("GCP_BIGQUERY_DATASET")
    GCP_BIGQUERY_URI: str = f"bigquery://{GOOGLE_CLOUD_PROJECT_NAME}/{GCP_BIGQUERY_DATASET}"

    # Google Cloud storage
    GCP_BUCKET_URL: str = getenv("GCP_BUCKET_URL")
    GCP_BUCKET_NAME: str = getenv("GCP_BUCKET_NAME")
    GCP_BUCKET_FOLDER: list = [f'{TODAY_DATE.year}/{TODAY_DATE.strftime("%m")}']

    # Plausible Analytics
    PLAUSIBLE_STATS_ENDPOINT: str = "https://plausible.io/api/v1/stats/breakdown"
    PLAUSIBLE_API_TOKEN: str = getenv("PLAUSIBLE_API_TOKEN")

    # Ghost
    GHOST_API_VERSION: str = "v3.0"
    GHOST_BASE_URL: str = getenv("GHOST_BASE_URL")
    GHOST_ADMIN_API_URL: str = f"{GHOST_BASE_URL}/ghost/api/admin"
    GHOST_CONTENT_API_URL: str = f"{GHOST_BASE_URL}/ghost/api/content"
    GHOST_API_USERNAME: str = getenv("GHOST_API_USERNAME")
    GHOST_API_PASSWORD: str = getenv("GHOST_API_PASSWORD")
    GHOST_CLIENT_ID: str = getenv("GHOST_CLIENT_ID")
    GHOST_ADMIN_API_KEY: str = getenv("GHOST_ADMIN_API_KEY")
    GHOST_CONTENT_API_KEY: str = getenv("GHOST_CONTENT_API_KEY")
    GHOST_API_EXPORT_URL: str = f"{GHOST_BASE_URL}/admin/db/"
    GHOST_NETLIFY_BUILD_HOOK: str = getenv("GHOST_NETLIFY_BUILD_HOOK")

    GHOST_ADMIN_USER_ID: str = "1"

    # Mailgun
    MAILGUN_EMAIL_SERVER: str = getenv("MAILGUN_EMAIL_SERVER")
    MAILGUN_NEWSLETTER_TEMPLATE: str = getenv("MAILGUN_NEWSLETTER_TEMPLATE")
    MAILGUN_SENDER_API_KEY: str = getenv("MAILGUN_SENDER_API_KEY")
    MAILGUN_FROM_SENDER_EMAIL: EmailStr = getenv("MAILGUN_FROM_SENDER_EMAIL")
    MAILGUN_FROM_SENDER_NAME: str = getenv("MAILGUN_FROM_SENDER_NAME")
    MAILGUN_PERSONAL_EMAIL: str = getenv("MAILGUN_PERSONAL_EMAIL")
    MAILGUN_PASSWORD: str = getenv("MAILGUN_PASSWORD")
    MAILGUN_SUBJECT_LINE: str = "To Hack or to Slack; That is the Question."

    MAILGUN_CONF: ClassVar = ConnectionConfig(
        MAIL_USERNAME="api",
        MAIL_STARTTLS=True,
        MAIL_SSL_TLS=True,
        MAIL_PASSWORD=MAILGUN_PASSWORD,
        MAIL_PORT=587,
        MAIL_SERVER=MAILGUN_EMAIL_SERVER,
        MAIL_FROM=MAILGUN_FROM_SENDER_EMAIL,
    )

    # Mixpanel
    MIXPANEL_API_TOKEN: str = getenv("MIXPANEL_API_TOKEN")

    # Twilio
    TWILIO_SENDER_PHONE: str = getenv("TWILIO_SENDER_PHONE")
    TWILIO_RECIPIENT_PHONE: str = getenv("TWILIO_RECIPIENT_PHONE")
    TWILIO_AUTH_TOKEN: str = getenv("TWILIO_AUTH_TOKEN")
    TWILIO_ACCOUNT_SID: str = getenv("TWILIO_ACCOUNT_SID")

    # Github
    GITHUB_USERNAME: str = getenv("GH_USERNAME")
    GITHUB_API_KEY: str = getenv("GH_API_KEY")


settings = Settings()
