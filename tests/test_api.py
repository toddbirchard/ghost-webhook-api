from fastapi.testclient import TestClient

from app import api
from config import basedir
from clients.log import LOGGER


client = TestClient(api)


def test_api_docs():
    response = client.get("/")
    assert response.status_code == 200
    assert response.headers.get("Content-Type") == "text/html; charset=utf-8"


def test_batch_lynx_previews(rdbms):
    sql_file = open(f"{basedir}/app/posts/queries/selects/lynx_bookmarks.sql", "r")
    query = sql_file.read()
    posts = rdbms.execute_query(query, "hackers_prod").fetchall()
    LOGGER.info(type(posts))
    assert isinstance(posts, list)
