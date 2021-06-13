from typing import List, Optional, Tuple

from clients import gcs, ghost
from log import LOGGER


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


def update_add_lynx_image(body: dict) -> dict:
    """
    Assign random Lynx feature image to Lynx post.

    :param body: JSON body representing Ghost post.
    :type body: dict
    :returns: dict
    """
    feature_image = gcs.fetch_random_lynx_image()
    body["posts"][0].update(
        {
            "feature_image": feature_image,
            "og_image": feature_image,
            "twitter_image": feature_image,
        }
    )
    LOGGER.info(
        f"Fetched random Lynx image `{feature_image}` for `{body['posts'][0]['slug']}`"
    )
    return body


def update_html_ssl_links(html: str, body: dict) -> dict:
    """
    Replace hyperlinks in post with SSL equivalents

    :param html: Raw post html.
    :type html: str
    :param body: JSON body representing Ghost post.
    :type body: dict
    :returns: dict
    """
    html = html.replace("http://", "https://")
    body["posts"][0].update({"html": html})
    LOGGER.info(f"Replaced unsecure links in post `{body['posts'][0]['slug']}`")
    return body


def update_metadata_images(feature_image: str, body: dict) -> dict:
    """
    Update OG and Twitter images to match feature image.

    :param feature_image: Post feature image url.
    :type feature_image: str
    :param body: JSON body representing Ghost post.
    :type body: dict
    :returns: dict
    """
    body["posts"][0].update({"og_image": feature_image, "twitter_image": feature_image})
    LOGGER.info(f"Updated metadata images for post `{body['posts'][0]['slug']}`")
    return body
