"""Author management."""
from fastapi import APIRouter
from fastapi.responses import JSONResponse

from clients import sms
from config import settings
from database import ghost_db
from database.read_sql import collect_sql_queries
from database.schemas import PostUpdate
from log import LOGGER

router = APIRouter(prefix="/authors", tags=["authors"])


@router.get(
    "/update/",
    summary="Sanitize author images & metadata.",
    description="Update all authors to have correct CDN urls & sanitized metadata.",
)
async def authors_bulk_update_metadata() -> JSONResponse:
    """
    Bulk update author images to use CDN URLs.

    :returns: JSONResponse
    """
    update_author_queries = collect_sql_queries("users")
    update_author_results = ghost_db.execute_queries(update_author_queries)
    LOGGER.success(f"Updated author metadata for {len(update_author_results)} authors.")
    return JSONResponse(
        content={"authors": update_author_results},
        status_code=200,
    )


@router.post("/post/created/")
async def author_post_created(post_update: PostUpdate) -> JSONResponse:
    """
    Notify admin when new authors create a new post.

    :param PostUpdate post_update: Post object generated upon update.

    :returns: JSONResponse
    """
    data = post_update.post.current
    title = data.title
    author_name = data.primary_author.name
    primary_author_id = data.primary_author.id
    authors = data.authors
    if primary_author_id not in (
        settings.GHOST_ADMIN_USER_ID,
        settings.GHOST_ADMIN_USER_ID,
    ):
        msg = f"{author_name} just created a post: `{title}`."
        sms.send_message(msg)
        return JSONResponse(content=msg, status_code=200)
    elif primary_author_id == settings.GHOST_ADMIN_USER_ID and len(authors) > 1:
        msg = f"{author_name} just updated one of your posts: `{title}`."
        sms.send_message(msg)
        return JSONResponse(content=msg, status_code=200)
    return JSONResponse(content=f"Author is {author_name}, carry on.", status_code=204)


@router.post("/post/updated/")
async def author_post_tampered(post_update: PostUpdate) -> JSONResponse:
    """
    Notify admin when new authors edit an admin post.

    :param PostUpdate post_update: Post object generated upon update.

    :returns: JSONResponse
    """
    data = post_update.post.current
    title = data.title
    primary_author_id = data.primary_author.id
    authors = data.authors
    if primary_author_id == settings.GHOST_ADMIN_USER_ID and len(authors) > 1:
        other_authors = [author.name for author in authors if author.id != settings.GHOST_ADMIN_USER_ID]
        msg = f"{', '.join(other_authors)} updated you post: `{title}`."
        sms.send_message(msg)
        return JSONResponse(content=msg, status_code=200)
    return JSONResponse(
        content=f"{data.primary_author.name} edited one of their own posts, carry on.",
        status_code=200,
    )
