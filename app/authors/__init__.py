"""Author management."""
from fastapi import APIRouter
from fastapi.responses import JSONResponse

from app.posts.models import PostUpdate
from clients import sms
from clients.log import LOGGER

router = APIRouter(prefix="/authors", tags=["authors"])


@router.post("/post")
def author_post_created(post: PostUpdate):
    """Notify admin user upon author post creation."""
    data = request.get_json()["post"]["current"]
    title = data.get("title")
    author_name = data["primary_author"]["name"]
    primary_author = data["primary_author"]["id"]
    authors = data["authors"]
    if primary_author == 1 and len(authors) > 1:
        msg = f"{author_name} just updated a post: `{title}`."
        LOGGER.info(f"SMS notification triggered by post edit: {msg}")
        sms.send_message(msg)
        return msg
    return JSONResponse(
        f"Author is {author_name}, carry on.", 204, {"content-type:": "text/plain"}
    )
