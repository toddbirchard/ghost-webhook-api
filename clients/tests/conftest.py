import pytest
from config import Settings
from clients.ghost import Ghost
from clients.mail import Mailgun


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