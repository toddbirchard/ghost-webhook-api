import pytest

from clients import ghost, mailgun
from clients.log import LOGGER


@pytest.fixture
def comment_body():
    return {
        "comment_id": "123",
        "user_name": "Loser",
        "user_avatar": None,
        "user_id": None,
        "body": "This is a test comment!",
        "post_id": "5dc42cb812c9ce0d63f5c0c3",
        "post_slug": "hostile-extraction-of-tableau-server-data",
        "user_role": None,
        "created_at": None,
    }


def test_comment_email(comment_body):
    post = ghost.get_post("5dc42cb812c9ce0d63f5c0c3")
    response = mailgun.send_comment_notification_email(post, comment_body)
    LOGGER.info(response)
    assert post["posts"][0]["primary_author"]["name"] == "Todd Birchard"
    assert comment_body["user_name"] != post["posts"][0]["primary_author"]["name"]
    assert response.status_code == 200
