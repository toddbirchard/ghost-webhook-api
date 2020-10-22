import pytest

from api import init_api


@pytest.fixture
def api():
    api = init_api()
    return api
