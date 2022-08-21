"""Parse Comment into JSON response."""
from database.models import Comment


def parse_comment_json(comment: Comment) -> dict:
    """
    Transform `Comment` object to JSON.

    :param Comment comment: Comment on a post left by a user.

    :returns: dict
    """
    return {
        "id": comment.id,
        "user_id": comment.user_id,
        "username": comment.user_name,
        "email": comment.user_email,
        "role": comment.user_role,
        "body": comment.body,
        "post_id": comment.post_id,
        "post_slug": comment.post_slug,
        "created_at": str(comment.created_at),
    }