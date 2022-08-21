"""Methods for updating Ghost post content or metadata."""
from typing import List, Optional, Tuple

from clients import ghost
from log import LOGGER


def update_mobiledoc(post_id: str, mobiledoc: str) -> Tuple[str, int]:
    """
    Update Lynx post with proper embedded URLs.

    :param str post_id: ID of post to be updated.
    :param str mobiledoc: Mobiledoc encoded as string with escaped characters.

    :returns: Tuple[str, int]
    """
    ghost_post = ghost.get_post(post_id)
    body = {
        "posts": [
            {
                "mobiledoc": mobiledoc,
                "status": ghost_post.status,
                "updated_at": ghost_post.updated_at,
            }
        ]
    }
    return ghost.update_post(ghost_post["id"], body, ghost_post["slug"])


def update_metadata(post_dicts: List[dict]) -> List[Optional[dict]]:
    """
    Update Ghost posts with bad or missing metadata.

    :param List[dict] post_dicts: Ghost posts as list of dictionaries.

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
        code = ghost.update_post(post_dict["id"], body, post["slug"])
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


def update_html_ssl_urls(html: str, body: dict, slug: str) -> dict:
    """
    Replace hyperlinks in post with SSL equivalents.

    :param str html: Raw post html.
    :param dict body: JSON body representing Ghost post.
    :param str slug: Unique post identifier for logging purposes.

    :returns: dict
    """
    html = html.replace("http://", "https://")
    body["posts"][0].update({"html": html})
    LOGGER.info(f"Replaced unsecure URLs in post `{slug}`")
    return body


def update_metadata_images(feature_image: str, body: dict, slug: str) -> dict:
    """
    Update OG and Twitter images to match feature image.

    :param str feature_image: Post feature image url.
    :param dict body: JSON body representing Ghost post.
    :param str slug: Unique post identifier.

    :returns: dict
    """
    body["posts"][0].update({"og_image": feature_image, "twitter_image": feature_image})
    LOGGER.info(f"Updated metadata images for post `{slug}`")
    return body
