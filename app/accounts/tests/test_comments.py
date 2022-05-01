from random import randint

import pytest

from app.accounts.comments import parse_comment
from config import settings
from database.schemas import NewComment


@pytest.fixture
def comment() -> NewComment:
    comment_randomizer = randint(1, 9999999999)
    return NewComment(
        post_id="61304d8374047afda1c21693",
        post_slug="python-virtualenv-virtualenvwrapper",
        user_id="8c06d6d7-2b02-4f4f-b8df-2ca5d16c0385",
        user_name="Todd Birchard",
        user_avatar="https://avatars3.githubusercontent.com/u/2747442?v=4",
        user_email=settings.MAILGUN_PERSONAL_EMAIL,
        author_id="1",
        body=f"TEST: I'm a fan of this post! Random comment #{comment_randomizer}",
    )


@pytest.fixture
def comment_no_username() -> NewComment:
    comment_randomizer = randint(1, 9999999999)
    return NewComment(
        post_id="61304d8374047afda1c21693",
        post_slug="python-virtualenv-virtualenvwrapper",
        user_id="8c06d6d7-2b02-4f4f-b8df-2ca5d16c0385",
        user_name=None,
        user_avatar="undefined",
        user_email=settings.MAILGUN_PERSONAL_EMAIL,
        author_id="1",
        body=f"TEST: I'm a fan of this post! I' also missing a username! Random comment #{comment_randomizer}",
    )


def test_comment_parser(ghost, comment: NewComment):
    post = ghost.get_post(comment.post_id)
    parsed_comment = parse_comment(ghost, comment, post)
    assert parsed_comment is not None
    assert type(parsed_comment) == dict
    assert len(parsed_comment.keys()) == 7
    assert parsed_comment["user_role"] == "author"


def test_comment_parser_missing_username(ghost, comment_no_username: NewComment):
    post = ghost.get_post(comment_no_username.post_id)
    parsed_comment = parse_comment(ghost, comment_no_username, post)
    # When empty, username is derived from user's Email
    assert comment_no_username.user_name is None
    assert comment_no_username.user_email is not None
    assert parsed_comment["user_name"] == comment_no_username.user_email.split("@")[0]
    assert "@" not in parsed_comment["user_name"]
    # Ensure avatars are stored as `None` when `undefined`
    assert parsed_comment["user_avatar"] is None
