"""Pytest fixtures for clients."""

import pytest
from google.cloud.bigquery import Client as gbqClient

from clients.ghost import Ghost
from clients.mail import Mailgun
from config import settings


@pytest.fixture
def ghost() -> Ghost:
    return Ghost(
        admin_api_url=settings.GHOST_ADMIN_API_URL,
        api_version=settings.GHOST_API_VERSION,
        content_api_url=settings.GHOST_CONTENT_API_URL,
        client_id=settings.GHOST_CLIENT_ID,
        client_secret=settings.GHOST_ADMIN_API_KEY,
        content_api_key=settings.GHOST_CONTENT_API_KEY,
    )


@pytest.fixture
def mailgun() -> Mailgun:
    return Mailgun(
        settings.MAILGUN_EMAIL_SERVER,
        settings.MAILGUN_FROM_SENDER_EMAIL,
        settings.MAILGUN_SENDER_API_KEY,
    )


@pytest.fixture
def gbq() -> gbqClient:
    return gbqClient(
        project=settings.GCP_PROJECT_NAME,
        credentials=settings.GCP_CREDENTIALS,
    )
