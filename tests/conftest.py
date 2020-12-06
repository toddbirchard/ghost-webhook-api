import pytest
from config import Settings
from clients.sms import Twilio
from clients.ghost import Ghost
from clients.mail import Mailgun
from clients.storage import GCS
from database.sql_db import Database


@pytest.fixture
def sms():
    return Twilio(
        sid=Settings().TWILIO_ACCOUNT_SID,
        token=Settings().TWILIO_AUTH_TOKEN,
        recipient=Settings().TWILIO_RECIPIENT_PHONE,
        sender=Settings().TWILIO_SENDER_PHONE,
    )


@pytest.fixture
def ghost():
    return Ghost(
        admin_api_url=Settings().GHOST_ADMIN_API_URL,
        content_api_url=Settings().GHOST_CONTENT_API_URL,
        client_id=Settings().GHOST_CLIENT_ID,
        client_secret=Settings().GHOST_ADMIN_API_KEY,
        netlify_build_url=Settings().GHOST_NETLIFY_BUILD_HOOK,
    )


@pytest.fixture
def mailgun():
    return Mailgun(
        Settings().MAILGUN_EMAIL_SERVER,
        Settings().MAILGUN_FROM_SENDER,
        Settings().MAILGUN_API_KEY,
    )


@pytest.fixture
def gcs():
    return GCS(
        bucket_name=Settings().GCP_BUCKET_NAME,
        bucket_url=Settings().GCP_BUCKET_URL,
        bucket_lynx=Settings().GCP_LYNX_DIRECTORY,
    )


@pytest.fixture
def rdbms():
    return Database(
        uri=Settings().SQLALCHEMY_DATABASE_URI, args=Settings().SQLALCHEMY_ENGINE_OPTIONS
    )
