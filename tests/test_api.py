from fastapi.testclient import TestClient

from app import api

client = TestClient(api)


def test_api_docs():
    response = client.get("/")
    assert response.status_code == 200
    assert response.headers.get("Content-Type") == "text/html; charset=utf-8"
