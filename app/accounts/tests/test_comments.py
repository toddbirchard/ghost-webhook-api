from app.accounts.comments import parse_comment
from clients import ghost
from log import LOGGER


def test_parse_comment(comment_missing_username):
    post = ghost.get_post(comment_missing_username.post_id)
    comment_parsed = parse_comment(comment_missing_username, post)
    assert comment_parsed["user_name"] is not None
    assert (
        comment_parsed["user_name"] == comment_missing_username.user_email.split("@")[0]
    )
    assert "@" not in comment_parsed["user_name"]
    LOGGER.debug(comment_parsed)
