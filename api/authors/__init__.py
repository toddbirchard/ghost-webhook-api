"""Author management."""
from flask import current_app as api
from flask import make_response, request

from clients import sms
from clients.log import LOGGER


@LOGGER.catch
@api.route("/authors/post", methods=["POST"])
def author_post_created():
    """Notify admin upon author post creation."""
    data = request.get_json()["post"]["current"]
    title = data["title"]
    image = data.get("feature_image", None)
    status = data.get("status")
    author_name = data["primary_author"]["name"]
    author_slug = data["primary_author"]["slug"]
    if author_slug != "todd":
        action_taken = "UPDATED"
        if status != "draft":
            action_taken = "PUBLISHED"
        msg = f"{author_name} just {action_taken} a post: `{title}`."
        if image is None and data["primary_tag"]["slug"] != "roundup":
            msg = msg.join([msg, "Needs feature image."])
            LOGGER.info(f"SMS notification triggered by post edit: {msg}")
            sms.send_message(msg)
        return make_response(msg, 200)
    return make_response(
        f"Author is {author_name}, carry on.", 204, {"content-type:": "text/plain"}
    )
