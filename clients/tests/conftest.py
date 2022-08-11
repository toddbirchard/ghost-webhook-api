import pytest
from google.cloud import bigquery

from clients.ghost import Ghost
from clients.mail import Mailgun
from config import settings


@pytest.fixture
def ghost():
    return Ghost(
        admin_api_url=settings.GHOST_ADMIN_API_URL,
        api_version=settings.GHOST_API_VERSION,
        content_api_url=settings.GHOST_CONTENT_API_URL,
        client_id=settings.GHOST_CLIENT_ID,
        client_secret=settings.GHOST_ADMIN_API_KEY,
        netlify_build_url=settings.GHOST_NETLIFY_BUILD_HOOK,
        content_api_key=settings.GHOST_CONTENT_API_KEY,
    )


@pytest.fixture
def mailgun():
    return Mailgun(
        settings.MAILGUN_EMAIL_SERVER,
        settings.MAILGUN_FROM_SENDER_EMAIL,
        settings.MAILGUN_SENDER_API_KEY,
    )


@pytest.fixture
def gbq():
    return bigquery.Client(
        project=settings.GOOGLE_CLOUD_PROJECT_NAME,
        credentials=settings.GOOGLE_CLOUD_CREDENTIALS,
    )
