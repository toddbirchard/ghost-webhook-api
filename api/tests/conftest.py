from .. import init_api
import pytest


@pytest.fixture
def app():
    app = init_api()
    return app
