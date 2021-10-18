import pytest

from database.schemas import NewComment


@pytest.fixture
def comment_missing_username() -> NewComment:
    return NewComment(
        id=9999999999999,
        post_id="61304d8374047afda1c21900",
        post_slug="deploy-flask-uwsgi-nginx",
        user_id="8c06d6d7-2b02-4f4f-b8df-2ca5d16c0385",
        user_name=None,
        user_avatar="https://avatars3.githubusercontent.com/u/2747442?v=4",
        user_email="todd@gmail.com",
        body="I'm a fan of your flask series!",
        created_at="2020-12-20T08:58:49.488Z",
        author_name="todd",
    )
