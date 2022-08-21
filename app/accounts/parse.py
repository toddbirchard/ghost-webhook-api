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
        "user_name": comment.user_name,
        "user_email": comment.user_email,
        "user_role": comment.user_role,
        "user_avatar": comment.user.avatar_url,
        "user_created_at": str(comment.user.created_at),
        "post_id": comment.post_id,
        "post_slug": comment.post_slug,
        "comment_body": comment.body,
        "comment_created_at": str(comment.created_at),
    }
