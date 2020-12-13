from typing import List, Tuple

from clients import ghost


def update_mobiledoc(post: dict, mobiledoc: str) -> Tuple[str, int]:
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


def batch_update_metadata(post_dicts: List[dict]):
    """Update Ghost posts with bad or missing metadata."""
    updated_posts = []
    for post_dict in post_dicts:
        post = ghost.get_post(post_dict["id"])
        body = {
            "posts": [
                {
                    "meta_title": post["title"],
                    "og_title": post["title"],
                    "twitter_title": post["title"],
                    "meta_description": post["custom_excerpt"],
                    "twitter_description": post["custom_excerpt"],
                    "og_description": post["custom_excerpt"],
                    "updated_at": post["updated_at"],
                }
            ]
        }
        response, code = ghost.update_post(post_dict["id"], body, post["slug"])
        if code == 200:
            updated_posts.append(
                {
                    "meta_title": post["title"],
                    "og_title": post["title"],
                    "twitter_title": post["title"],
                    "meta_description": post["custom_excerpt"],
                    "twitter_description": post["custom_excerpt"],
                    "og_description": post["custom_excerpt"],
                }
            )
    return updated_posts
