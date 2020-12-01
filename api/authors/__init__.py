"""Author management."""
from flask import current_app as api
from flask import make_response, request

from clients import sms
from clients.log import LOGGER


@LOGGER.catch
@api.route("/authors/post", methods=["POST"])
def author_post_created():
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
        return make_response(msg, 200, {"content-type:": "text/plain"})
    return make_response(
        f"Author is {author_name}, carry on.", 204, {"content-type:": "text/plain"}
    )
