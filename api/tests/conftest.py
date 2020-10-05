from api import init_api
import pytest

@pytest.fixture
def api():
    api = init_api()
    return api
