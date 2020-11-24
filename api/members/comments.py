from datetime import datetime
from typing import Optional

from clients import ghost, mailgun


def parse_comment(data: dict, post: dict):
    """Parse incoming user comment."""
    return {
        "comment_id": data.get("id"),
        "user_name": data.get("user_name"),
        "user_avatar": data.get("user_avatar"),
        "user_id": data.get("user_id"),
        "body": data.get("body"),
        "post_id": data.get("post_id"),
        "post_slug": data.get("post_slug"),
        "user_role": get_user_role(data, post),
        "created_at": datetime.strptime(
            data.get("created_at").replace("Z", ""), "%Y-%m-%dT%H:%M:%S.%f"
        ),
    }


def get_user_role(data: dict, post: dict) -> Optional[str]:
    """Determine role of comment author."""
    authors = ghost.get_authors()
    if post:
        if post["primary_author"]["email"] == data.get("user_email"):
            return "author"
        elif data.get("user_email") in authors:
            return "moderator"
    return None
