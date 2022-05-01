import pytest


@pytest.fixture
def comment_body():
    return {
        "post_id": "61304d8374047afda1c2168b",
        "post_slug": "welcome-to-hackers-and-slackers",
        "user_id": "8c06d6d7-2b02-4f4f-b8df-2ca5d16c0385",
        "user_name": "Fake user 123",
        "user_avatar": "https://avatars3.githubusercontent.com/u/2747442?v=4",
        "user_email": "person@example.com",
        "user_role": None,
        "author_id": "1",
        "body": "This is a test comment!",
    }


def test_comment_email(comment_body, ghost, mailgun):
    post = ghost.get_post("61304d8374047afda1c2168b")
    author_name = post["primary_author"]["name"]
    author_email = post["primary_author"]["email"]
    recipient = [f"{author_name} <{author_email}>"]
    email_notification = mailgun.email_notification_new_comment(
        post, recipient, comment_body, test_mode=True
    )
    assert post["primary_author"]["name"] == "Todd Birchard"
    assert post["primary_author"]["email"] is not None
    assert comment_body["user_name"] != post["primary_author"]["name"]
    assert email_notification["status"]["sent"] is True
    assert email_notification["status"]["code"] == 200
    assert email_notification["status"]["error"] is None
