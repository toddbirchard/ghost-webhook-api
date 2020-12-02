from datetime import datetime
from typing import Optional

from .models import Comment
from clients import ghost


def parse_comment(comment: Comment, post: dict) -> dict:
    """Parse incoming user comment."""
    return {
        "comment_id": comment.id,
        "user_name": comment.user_name,
        "user_avatar": comment.user_avatar,
        "user_id": comment.user_id,
        "body": comment.body,
        "post_id": comment.post_id,
        "post_slug": comment.post_slug,
        "user_role": get_user_role(comment, post),
        "created_at": datetime.strptime(
            comment.created_at.replace("Z", ""), "%Y-%m-%dT%H:%M:%S.%f"
        ),
    }


def get_user_role(comment: Comment, post: dict) -> Optional[str]:
    """Determine whether a commenter is the post author or site moderator."""
    authors = ghost.get_authors()
    if post:
        if post["primary_author"]["email"] == comment.user_email:
            return "author"
        elif comment.user_email in authors:
            return "moderator"
    return None
