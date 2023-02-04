"""Enrich post metadata."""
from datetime import datetime, timedelta
from time import sleep

from fastapi import APIRouter
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse

from app.moment import get_current_datetime, get_current_time
from app.posts.metadata import optimize_posts_metadata
from app.posts.update import update_html_ssl_urls, update_metadata_images
from clients import ghost
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
async def update_post(post_update: PostUpdate) -> JSONResponse:
    """
    Enrich post metadata upon update.

    :param PostUpdate post_update: Request to update Ghost post.

    :returns: JSONResponse
    """
    previous_update = post_update.post.previous
    if previous_update:
        current_time = get_current_datetime()
        previous_update_date = datetime.strptime(str(previous_update.updated_at), "%Y-%m-%dT%H:%M:%S.000Z")
        if previous_update_date and current_time - previous_update_date < timedelta(seconds=5):
            LOGGER.warning("Post update ignored as post was just updated.")
            raise HTTPException(status_code=422, detail="Post update ignored as post was just updated.")
    post = post_update.post.current
    slug = post.slug
    feature_image = post.feature_image
    html = post.html
    body = {
        "posts": [
            {
                "meta_title": post.title,
                "og_title": post.title,
                "twitter_title": post.title,
                "meta_description": post.custom_excerpt,
                "twitter_description": post.custom_excerpt,
                "og_description": post.custom_excerpt,
                "updated_at": get_current_time(),
            }
        ]
    }
    if html and "http://" in html:
        body = update_html_ssl_urls(html, body, slug)
    if feature_image is not None:
        body = update_metadata_images(feature_image, body, slug)
    sleep(1)
    time = get_current_time()
    body["posts"][0]["updated_at"] = time
    response, code = ghost.update_post(post.id, body, post.slug)
    LOGGER.success(f"Successfully updated post `{slug}`: {body}")
    return JSONResponse({str(code): response})


@router.get(
    "/",
    summary="Sanitize metadata for all posts.",
    description="Ensure all posts have properly optimized metadata.",
    response_model=PostBulkUpdate,
)
async def batch_update_metadata() -> JSONResponse:
    """
    Run SQL queries to sanitize metadata for all posts.

    :returns: JSONResponse
    """
    posts_metadata_updated, posts_metadata_added = optimize_posts_metadata()
    return JSONResponse(
        content=f"Inserted {posts_metadata_added}; Updated{posts_metadata_updated}",
        status_code=200,
    )


@router.get("/backup/")
async def backup_database():
    """Export JSON backup of database."""
    json = ghost.get_json_backup()
    return json


@router.get(
    "/post/",
    summary="Get a post.",
)
async def get_single_post(post_id: str) -> JSONResponse:
    """
    Request to get Ghost post.

    :param str post_id: Post to fetch

    :returns: JSONResponse
    """
    if post_id is None:
        raise HTTPException(status_code=422, detail="Post ID required to test endpoint.")
    return JSONResponse(ghost.get_post(post_id))


@router.get(
    "/all/",
    summary="Get all post URLs.",
)
async def get_all_posts() -> JSONResponse:
    """
    List all published Ghost posts.

    :returns: JSONResponse
    """
    posts = ghost.get_all_posts()
    LOGGER.success(f"Fetched all {len(posts)} Ghost posts: {posts}")
    return JSONResponse(
        posts,
        status_code=200,
    )
