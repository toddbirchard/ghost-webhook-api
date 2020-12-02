import pytest
from flask import url_for


def test_app(client):
    assert client.get(url_for("health_check")).status_code == 200
