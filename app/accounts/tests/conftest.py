import pytest

from clients.ghost import Ghost
from config import settings


@pytest.fixture
def ghost():
    return Ghost(
        admin_api_url=settings.GHOST_ADMIN_API_URL,
        content_api_url=settings.GHOST_CONTENT_API_URL,
        client_id=settings.GHOST_CLIENT_ID,
        client_secret=settings.GHOST_ADMIN_API_KEY,
        netlify_build_url=settings.GHOST_NETLIFY_BUILD_HOOK,
        content_api_key=settings.GHOST_CONTENT_API_KEY,
    )
