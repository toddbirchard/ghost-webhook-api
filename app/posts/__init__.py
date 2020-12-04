"""Routes to transform post data."""
from datetime import datetime, timedelta
from time import sleep

from fastapi import APIRouter
from fastapi.responses import JSONResponse

from app.moment import get_current_datetime, get_current_time
from clients import gcs, ghost
from clients.log import LOGGER
from database import rdbms

from .lynx.parse import generate_bookmark_html, generate_link_previews
from .models import Post, PostUpdate
from .read import get_queries

router = APIRouter(prefix="/posts", tags=["posts"])


@router.post(
    "/update",
    summary="Optimize a single post image.",
    description="Generate retina and mobile feature image for a single post upon update.",
)
def update_post(post_update: PostUpdate):
    """Enrich post metadata upon update."""
    previous_update = post_update.post.previous
    if previous_update:
        current_time = get_current_datetime()
        previous_update_date = datetime.strptime(
            previous_update["updated_at"], "%Y-%m-%dT%H:%M:%S.000Z"
        )
        if previous_update_date and current_time - previous_update_date < timedelta(
            seconds=5
        ):
            LOGGER.warning("Post update ignored as post was just updated.")
            return "Post update ignored as post was just updated."
    post = post_update.post.current
    post_id = post.id
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
        feature_image = gcs.fetch_random_lynx_image()
        body["posts"][0].update(
            {
                "feature_image": feature_image,
                "og_image": feature_image,
                "twitter_image": feature_image,
            }
        )
    if html and "http://" in html:
        html = html.replace("http://", "https://")
        body["posts"][0].update({"html": html})
        LOGGER.info(f"Resolved unsecure links in post `{slug}`")
    """if html and ('kg-card' not in html):
        doc = generate_link_previews(post)
        LOGGER.info(f'Generated Previews for Lynx post {slug}.')
        body['posts'][0].update({
            "mobiledoc": doc
        })"""
    # Update image meta tags
    if feature_image is not None:
        body["posts"][0].update(
            {"og_image": feature_image, "twitter_image": feature_image}
        )
    if body["posts"][0].mobiledoc:
        sleep(1)
        time = get_current_time()
        body["posts"][0]["updated_at"] = time
    response, code = ghost.update_post(post_id, body, slug)
    return {str(code): response}


@router.post("/test/html")
def test_bookmark_cards(post_update: PostUpdate):
    """Placeholder endpoint to test accuracy of scraping output"""
    post = post_update.post.current
    html = post.html
    primary_tag = post.primary_tag
    if html and ("kg-card" not in html) and primary_tag is not None:
        doc = generate_bookmark_html(html)
        return doc


@router.post("/test/mobiledoc")
def test_mobiledoc_cards(post_update: PostUpdate):
    post = post_update.post.current
    html = post.html
    primary_tag = post.primary_tag
    if html and ("kg-card" not in html):
        doc = generate_link_previews(post.__dict__)
        LOGGER.info(doc)
        return doc


@router.post("/embed")
def post_link_previews(post_update: PostUpdate):
    """Render anchor tag link previews."""
    post = post_update.post.current
    post_id = post.id
    slug = post.slug
    html = post.html
    previous = post_update.post.previous
    primary_tag = post.primary_tag
    time = get_current_time()
    if primary_tag["slug"] == "roundup":
        if html is not None and "kg-card" not in html:
            if previous is not None and "kg-card" not in previous["html"]:
                doc = generate_link_previews(post.__dict__)
                LOGGER.info(f"Generated Previews for Lynx post {slug}: {doc}")
                body = {"posts": [{"mobiledoc": doc, "updated_at": time}]}
                response, code = ghost.update_post(post_id, body, slug)
                return {f"Updated {slug} with code {code}": doc}
        LOGGER.warning(f"Lynx post {slug} already contains previews.")
        return JSONResponse(
            {f"Lynx post {slug} already contains previews."},
            status_code=202,
            headers={"content-type": "text/plain"},
        )


@router.get("/update")
def post_metadata_sanitize():
    """Mass update post metadata."""
    queries = get_queries()
    results = rdbms.execute_queries(queries, "hackers_prod")
    LOGGER.success(f"Successfully ran queries: {queries}")
    return results


@router.get("/backup")
def backup_database():
    """Export JSON backup of database."""
    json = ghost.get_json_backup()
    return json
