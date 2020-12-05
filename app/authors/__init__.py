"""Author management."""
from fastapi import APIRouter
from fastapi.responses import JSONResponse

from clients import sms
from clients.log import LOGGER
from database.schemas import PostUpdate

router = APIRouter(prefix="/authors", tags=["authors"])


@router.post("/posts/update")
def author_post_created(post_update: PostUpdate):
    """Notify admin user upon author post creation."""
    data = post_update.post.current
    title = data.title
    author_name = data.primary_author.name
    primary_author_id = data.primary_author.id
    authors = data.authors
    if primary_author_id == "1" and len(authors) > 1:
        msg = f"{author_name} just updated an admin post: `{title}`."
        LOGGER.info(f"SMS notification triggered by post edit: {msg}")
        sms.send_message(msg)
        return msg
    return JSONResponse(
        f"Author is {author_name}, carry on.", 204, {"content-type:": "text/plain"}
    )


@router.post("/posts/created")
def author_post_created(post_update: PostUpdate):
    """Notify when new authors create their first post."""
    data = post_update.post.current
    title = data.title
    author_name = data.primary_author.name
    primary_author_id = data.primary_author.id
    if primary_author_id not in ("1", "5dc42cb612c9ce0d63f5bf39"):
        msg = f"{author_name} just updated a post: `{title}`."
        LOGGER.info(f"SMS notification triggered by post edit: {msg}")
        sms.send_message(msg)
        return msg
    return JSONResponse(
        f"Author is {author_name}, carry on.", 204, {"content-type:": "text/plain"}
    )
