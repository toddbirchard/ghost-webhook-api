from typing import Tuple

from clients import ghost


def update_post(post: dict, mobiledoc: str) -> Tuple[str, int]:
    """Update Lynx post with proper embedded links."""
    ghost_post = ghost.get_post(post["id"])
    body = {
        "posts": [
            {
                "mobiledoc": mobiledoc,
                "updated_at": ghost_post["updated_at"],
            }
        ]
    }
    return ghost.update_post(post["id"], body, post["slug"])
