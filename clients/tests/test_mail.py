import pytest

from log import LOGGER


@pytest.fixture
def comment_body():
    return {
        "comment_id": "123",
        "user_name": "Loser",
        "user_avatar": None,
        "user_id": None,
        "body": "This is a test comment!",
        "post_id": "61304d8374047afda1c2168b",
        "post_slug": "welcome-to-hackers-and-slackers",
        "user_role": None,
        "created_at": None,
    }


def test_comment_email(comment_body, ghost, mailgun):
    post = ghost.get_post("5dc42cb812c9ce0d63f5c0c3")
    response = mailgun.email_notification_new_comment(
        post, comment_body, test_mode=True
    )
    LOGGER.debug(response.content)

    assert post["primary_author"]["name"] == "Todd Birchard"
    assert post["primary_author"]["email"] is not None
    assert comment_body["user_name"] != post["primary_author"]["name"]
    assert response.status_code == 200
    assert response.json() is not None
