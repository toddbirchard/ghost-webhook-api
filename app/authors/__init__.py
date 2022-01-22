"""Author management."""
from fastapi import APIRouter
from fastapi.responses import JSONResponse

from clients import sms
from config import settings
from database.schemas import PostUpdate

router = APIRouter(prefix="/authors", tags=["authors"])


@router.post("/post/created")
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
        settings.GHOST_AUTHOR_TODD_ID,
        settings.GHOST_AUTHOR_TODD_ID,
    ):
        msg = f"{author_name} just created a post: `{title}`."
        sms.send_message(msg)
        return JSONResponse(msg, 200, {"content-type:": "text/plain"})
    elif primary_author_id == settings.GHOST_AUTHOR_TODD_ID and len(authors) > 1:
        msg = f"{author_name} just updated one of your posts: `{title}`."
        sms.send_message(msg)
        return JSONResponse(msg, 200, {"content-type:": "text/plain"})
    return JSONResponse(
        f"Author is {author_name}, carry on.", 204, {"content-type:": "text/plain"}
    )


@router.post("/post/updated")
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
    if primary_author_id == settings.GHOST_AUTHOR_TODD_ID and len(authors) > 1:
        other_authors = [
            author.name
            for author in authors
            if author.id != settings.GHOST_AUTHOR_TODD_ID
        ]
        msg = f"{', '.join(other_authors)} updated you post: `{title}`."
        sms.send_message(msg)
        return JSONResponse(msg, 200, {"content-type:": "text/plain"})
    return JSONResponse(
        f"{data.primary_author.name} edited one of their own posts, carry on.",
        200,
        {"content-type:": "text/plain"},
    )
