import pytest


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


def test_comment_email(comment_body, ghost, mailgun):
    post = ghost.get_post("5dc42cb812c9ce0d63f5c0c3")
    response = mailgun.send_comment_notification_email(post, comment_body)
    assert post["primary_author"]["name"] == "Todd Birchard"
    assert post["primary_author"]["email"] is not None
    assert comment_body["user_name"] != post["primary_author"]["name"]
    assert response.status_code == 200
    assert response.json() is not None
