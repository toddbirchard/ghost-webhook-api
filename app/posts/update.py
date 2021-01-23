from typing import List, Optional, Tuple

from clients import ghost


def update_mobiledoc(post_id: str, mobiledoc: str) -> Tuple[str, int]:
    """
    Update Lynx post with proper embedded links.

    :param post_id: ID of post to be updated.
    :type post_id: str
    :param mobiledoc: Mobiledoc encoded as string with escaped characters.
    :type mobiledoc: str

    :returns: Tuple[str, int]
    """
    ghost_post = ghost.get_post(post_id)
    body = {
        "posts": [
            {
                "mobiledoc": mobiledoc,
                "updated_at": ghost_post["updated_at"],
            }
        ]
    }
    return ghost.update_post(ghost_post["id"], body, ghost_post["slug"])


def update_metadata(post_dicts: List[dict]) -> List[Optional[dict]]:
    """
    Update Ghost posts with bad or missing metadata.

    :param post_dicts: Ghost posts as list of dictionaries.
    :type post_dicts: List[dict]
    :returns: List[Optional[dict]]
    """
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
