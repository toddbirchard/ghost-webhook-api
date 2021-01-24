"""Parse new comments from users."""
from datetime import datetime
from typing import Optional

from clients import ghost
from database.schemas import NewComment


def parse_comment(comment: NewComment, post: dict) -> dict:
    """
    Parse incoming user comment.

    :param comment: User-submitted comment.
    :type comment: Comment
    :param post: Post on which comment was published.
    :type post: dict
    :returns: dict
    """
    username = comment.user_name
    avatar = comment.user_avatar
    if comment.user_name is None and comment.user_email:
        username = comment.user_email.split("@")[0]
    if avatar == "undefined":
        avatar = None
    return {
        "user_name": username,
        "user_avatar": avatar,
        "user_id": comment.user_id,
        "body": comment.body,
        "post_id": comment.post_id,
        "post_slug": comment.post_slug,
        "user_role": get_user_role(comment, post),
        "created_at": datetime.strptime(
            comment.created_at.replace("Z", ""), "%Y-%m-%dT%H:%M:%S.%f"
        ),
    }


def get_user_role(comment: NewComment, post: dict) -> Optional[str]:
    """
    Determine if a commenter is a post author, site moderator, or regular user.

    :param comment: User-submitted comment.
    :type comment: Comment
    :param post: Post on which comment was published.
    :type post: dict
    :returns: Optional[str]
    """
    authors = ghost.get_authors()
    if post:
        if post["primary_author"]["email"] == comment.user_email:
            return "author"
        elif comment.user_email in authors:
            return "moderator"
    return None
