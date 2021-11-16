"""Ghost post enrichment of data."""
from datetime import datetime, timedelta
from time import sleep

from fastapi import APIRouter
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse

from app.moment import get_current_datetime, get_current_time
from app.posts.lynx.parse import batch_lynx_embeds, generate_link_previews
from app.posts.metadata import assign_img_alt, batch_assign_img_alt
from app.posts.update import (
    update_add_lynx_image,
    update_html_ssl_links,
    update_metadata,
    update_metadata_images,
)
from clients import ghost
from config import BASE_DIR
from database import rdbms
from database.read_sql import collect_sql_queries
from database.schemas import PostBulkUpdate, PostUpdate
from log import LOGGER

router = APIRouter(prefix="/posts", tags=["posts"])


@router.post(
    "/",
    summary="Optimize post metadata.",
    description="Performs multiple actions to optimize post SEO. \
                Generates meta tags, ensures SSL hyperlinks, and populates missing <img /> `alt` attributes.",
    response_model=PostUpdate,
)
async def update_post(post_update: PostUpdate):
    """
    Enrich post metadata upon update.

    :param PostUpdate post_update: Request to update Ghost post.

    """
    previous_update = post_update.post.previous
    if previous_update:
        current_time = get_current_datetime()
        previous_update_date = datetime.strptime(
            str(previous_update.updated_at), "%Y-%m-%dT%H:%M:%S.000Z"
        )
        LOGGER.debug(
            f"current_time=`{current_time}` previous_update_date=`{previous_update_date}`"
        )
        if previous_update_date and current_time - previous_update_date < timedelta(
            seconds=5
        ):
            LOGGER.warning("Post update ignored as post was just updated.")
            raise HTTPException(
                status_code=422, detail="Post update ignored as post was just updated."
            )
    post = post_update.post.current
    slug = post.slug
    title = post.title
    feature_image = post.feature_image
    custom_excerpt = post.custom_excerpt
    primary_tag = post.primary_tag
    html = post.html
    time = get_current_time()
    body = {
        "posts": [
            {
                "meta_title": title,
                "og_title": title,
                "twitter_title": title,
                "meta_description": custom_excerpt,
                "twitter_description": custom_excerpt,
                "og_description": custom_excerpt,
                "updated_at": time,
            }
        ]
    }
    if primary_tag.slug == "roundup" and feature_image is None:
        body = update_add_lynx_image(body, slug)
    if html and "http://" in html:
        body = update_html_ssl_links(html, body, slug)
    if feature_image is not None:
        body = update_metadata_images(feature_image, body, slug)
    if body["posts"][0].get("mobiledoc") is not None:
        mobiledoc = assign_img_alt(body["posts"][0]["mobiledoc"])
        body["posts"][0].update({"mobiledoc": mobiledoc})
    sleep(1)
    time = get_current_time()
    body["posts"][0]["updated_at"] = time
    response, code = ghost.update_post(post.id, body, post.slug)
    LOGGER.success(f"Successfully updated post `{slug}`: {body}")
    return {str(code): response}


@router.get(
    "/",
    summary="Sanitize metadata for all posts.",
    description="Ensure all posts have properly optimized metadata.",
    response_model=PostBulkUpdate,
)
async def batch_update_metadata():
    update_queries = collect_sql_queries("posts/updates")
    update_results = rdbms.execute_queries(update_queries, "hackers_dev")
    insert_posts = rdbms.execute_query_from_file(
        f"{BASE_DIR}/database/queries/posts/selects/missing_all_metadata.sql",
        "hackers_dev",
    )
    insert_results = update_metadata(insert_posts)
    LOGGER.success(
        f"Inserted metadata for {len(insert_results)} posts, updated {len(update_results.keys())}."
    )
    return {
        "inserted": {"count": len(insert_results), "posts": insert_results},
        "updated": {"count": len(update_results.keys()), "posts": update_results},
    }


"""@router.get(
    "/embed",
    summary="Batch create Lynx embeds.",
    description="Fetch raw Lynx post and generate embedded link previews.",
)
async def batch_lynx_previews():
    posts = fetch_raw_lynx_posts()
    result = batch_lynx_embeds(posts)
    return result"""


@router.post(
    "/embed",
    summary="Embed Lynx links.",
    description="Generate embedded link previews for a single Lynx post.",
)
async def post_link_previews(post_update: PostUpdate):
    """
    Render anchor tag link previews.

    :param PostUpdate post_update: Request to update Ghost post.
    """
    post = post_update.post.current
    post_id = post.id
    slug = post.slug
    html = post.html
    previous = post_update.post.previous
    primary_tag = post.primary_tag
    if primary_tag.slug == "roundup":
        if html is not None and "kg-card" not in html and previous is None:
            num_embeds, doc = generate_link_previews(post.__dict__)
            result = rdbms.execute_query(
                f"UPDATE posts SET mobiledoc = '{doc}' WHERE id = '{post_id}';",
                "hackers_dev",
            )
            LOGGER.info(f"Generated Previews for Lynx post {slug}: {doc}")
            return JSONResponse(
                {
                    f"Successfully updated lynx post `{slug}` with mobiledoc: {doc}; Result: {result}."
                },
                status_code=200,
                headers={"content-type": "text/plain"},
            )
        return JSONResponse(
            {f"Lynx post `{slug}` already contains previews."},
            status_code=202,
            headers={"content-type": "text/plain"},
        )


@router.get(
    "/embed",
    summary="Embed Lynx links.",
    description="Generate embedded link previews for a single Lynx post.",
)
async def test_post_link_previews(post_id: str):
    """
    Render anchor tag link previews.

    :param str post_id: ID of a Ghost post to fetch to test embedding lynx previews.
    """
    if post_id is None:
        raise HTTPException(
            status_code=422, detail="Post ID required to test endpoint."
        )
    post = ghost.get_post(post_id)
    slug = post.slug
    html = post.html
    time = get_current_time()
    primary_tag = post.primary_tag
    if primary_tag.slug == "roundup":
        if html is not None and "kg-card" not in html:
            num_embeds, doc = generate_link_previews(post.__dict__)
            body = {
                "posts": [
                    {
                        "meta_title": post.title,
                        "og_title": post.title,
                        "twitter_title": post.title,
                        "meta_description": post.custom_excerpt,
                        "twitter_description": post.custom_excerpt,
                        "og_description": post.custom_excerpt,
                        "updated_at": time,
                    }
                ]
            }
            result = ghost.update_post(post_id, body, slug)
            LOGGER.info(f"Generated Previews for Lynx post {slug}: {doc}")
            return result
        return JSONResponse(
            {f"Lynx post {slug} already contains previews."},
            status_code=202,
            headers={"content-type": "text/plain"},
        )


@router.get(
    "/alt",
    summary="Populate missing alt text for images.",
    description="Assign missing alt text to embedded images.",
)
async def assign_img_alt_attr():
    """Find <img>s missing alt text and assign `alt`, `title` attributes."""
    return batch_assign_img_alt()


@router.get("/backup")
async def backup_database():
    """Export JSON backup of database."""
    json = ghost.get_json_backup()
    return json


@router.get(
    "/post",
    summary="Get a post.",
)
async def get_single_post(post_id: str):
    """
    Request to get Ghost post.

    :param str post_id: Post to fetch
    """
    if post_id is None:
        raise HTTPException(
            status_code=422, detail="Post ID required to test endpoint."
        )
    return ghost.get_post(post_id)
