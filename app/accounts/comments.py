"""Parse new comments from users."""
from typing import Optional

from clients import ghost
from database.schemas import NewComment


def parse_comment(comment: NewComment, post: dict) -> dict:
    """
    Parse incoming user comment.

    :param Comment comment: User-submitted comment.
    :param dict post: Post on which comment was published.

    :returns: dict
    """
    username = comment.user_name
    avatar = comment.user_avatar
    if comment.user_name is None and comment.user_email:
        username = comment.user_email.split("@")[0]
    if avatar == "undefined":
        avatar = None
    return {
        "post_id": comment.post_id,
        "post_slug": comment.post_slug,
        "user_name": username,
        "user_avatar": avatar,
        "user_id": comment.user_id,
        "user_role": get_user_role(comment, post),
        "body": comment.body,
    }


def get_user_role(comment: NewComment, post: dict) -> Optional[str]:
    """
    Determine if a commenter is a post author, site moderator, or regular user.

    :param Comment comment: User-submitted comment.
    :param dict post: Post on which comment was published.

    :returns: Optional[str]
    """
    authors = ghost.get_all_authors()
    author_emails = [author["email"] for author in authors]
    if comment.user_email == post["primary_author"]["email"]:
        return "author"
    if comment.user_email in author_emails:
        return "moderator"
    return None
