from fastapi.testclient import TestClient

from app import api
from clients.log import LOGGER
from config import basedir, settings

client = TestClient(api)


def test_api_docs():
    response = client.get("/")
    assert response.status_code == 200
    assert response.headers.get("Content-Type") == "text/html; charset=utf-8"


def test_batch_lynx_previews(rdbms):
    sql_file = open(f"{basedir}/database/queries/posts/selects/lynx_bookmarks.sql", "r")
    query = sql_file.read()
    posts = rdbms.execute_query(query, "hackers_prod").fetchall()
    assert isinstance(posts, list)
    for post in posts:
        assert "lynx" in post["slug"]
        assert "Lynx" in post["title"]
        assert "bookmark" not in post["mobiledoc"]
        assert "kg-card" not in post["html"]
        LOGGER.info(post["title"])


def test_github_pr(github_pr_owner, github_pr_user):
    owner_response = client.post("/github/pr", json=github_pr_owner)
    assert owner_response.status_code == 200
    assert owner_response.json()["pr"]["status"] == "ignored"
    assert owner_response.json()["pr"]["trigger"]["type"] == "github"
    assert (
        owner_response.json()["pr"]["trigger"]["repo"]
        == github_pr_user["pull_request"]["head"]["repo"]["name"]
    )

    user_response = client.post("/github/pr", json=github_pr_user)
    assert user_response.status_code == 200
    assert user_response.json()["pr"]["trigger"]["type"] == "github"
    assert (
        user_response.json()["pr"]["trigger"]["repo"]
        == github_pr_user["pull_request"]["head"]["repo"]["name"]
    )
    assert user_response.json()["pr"]["status"] == "queued"
    assert user_response.json()["sms"]["phone_sender"] == settings.TWILIO_SENDER_PHONE


def test_github_issue(github_issue_user):
    user_response = client.post("/github/issue", json=github_issue_user)
    assert user_response.status_code == 200
    assert user_response.json()["issue"]["status"] == "queued"
    assert user_response.json()["issue"]["trigger"]["type"] == "github"
    assert (
        user_response.json()["issue"]["trigger"]["repo"]
        == github_issue_user["repository"]["name"]
    )
    assert (
        user_response.json()["issue"]["trigger"]["title"]
        == github_issue_user["issue"]["title"]
    )
    assert user_response.json()["sms"]["phone_sender"] == settings.TWILIO_SENDER_PHONE


def test_batch_insert_metadata():
    response = client.get("/posts")
    assert response.status_code == 200
    assert response.json().get("inserted") is not None
    assert response.json().get("updated") is not None


def assign_img_alt_attr():
    result = client.get("/posts/alt")
    LOGGER.info(result.json())
