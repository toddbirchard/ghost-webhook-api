import pytest

from app import init_api


@pytest.fixture
def api():
    api = init_api()
    return api
