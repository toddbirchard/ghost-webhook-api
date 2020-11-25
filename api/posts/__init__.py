"""Routes to transform post data."""
from datetime import datetime, timedelta
from time import sleep

from flask import current_app as api
from flask import jsonify, make_response, request

from api.moment import get_current_datetime, get_current_time
from clients import db, gcs, ghost
from clients.log import LOGGER

from .lynx.parse import generate_bookmark_html, generate_link_previews
from .read import get_queries


@LOGGER.catch
@api.route("/posts/update", methods=["POST"])
def update_post():
    """Update post metadata upon save."""
    data = request.get_json()
    if data:
        previous_update = data["post"].get("previous")
        if previous_update:
            current_time = get_current_datetime()
            previous_update_date = datetime.strptime(
                data["post"]["previous"]["updated_at"], "%Y-%m-%dT%H:%M:%S.000Z"
            )
            if (
                previous_update_date
                and current_time - previous_update_date < timedelta(seconds=5)
            ):
                LOGGER.warning("Post update ignored as post was just updated.")
                return make_response(
                    "Post update ignored as post was just updated.", 422
                )
        post = data["post"]["current"]
        post_id = post.get("id")
        slug = post.get("slug")
        title = post.get("title")
        feature_image = post.get("feature_image")
        custom_excerpt = post.get("custom_excerpt")
        primary_tag = post.get("primary_tag")
        html = post.get("html")
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
        if primary_tag.get("slug") == "roundup" and feature_image is None:
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
        if body["posts"][0].get("mobiledoc"):
            sleep(1)
            time = get_current_time()
            body["posts"][0]["updated_at"] = time
        response, code = ghost.update_post(post_id, body, slug)
        return make_response(jsonify({str(code): response}))
    LOGGER.warning("JSON body missing from request.")
    return make_response("JSON body missing from request.", 422)


@api.route("/posts/test/html", methods=["POST"])
def test_bookmark_cards():
    """Placeholder endpoint to test accuracy of scraping output"""
    data = request.get_json()
    post = data["post"]["current"]
    html = post.get("html")
    primary_tag = post.get("primary_tag")
    if html and ("kg-card" not in html) and primary_tag is not None:
        doc = generate_bookmark_html(html)
        return make_response(doc, 200, "")


@api.route("/posts/test/mobiledoc", methods=["POST"])
def test_mobiledoc_cards():
    data = request.get_json()
    post = data["post"]["current"]
    html = post.get("html")
    primary_tag = post.get("primary_tag")
    if html and ("kg-card" not in html):
        doc = generate_link_previews(post)
        LOGGER.info(doc)
        return make_response(doc, 200, "")


@LOGGER.catch
@api.route("/posts/embed", methods=["POST"])
def post_link_previews():
    """Render anchor tag link previews."""
    post = request.get_json()["post"]["current"]
    post_id = post.get("id")
    slug = post.get("slug")
    html = post.get("html")
    previous = post.get("previous")
    primary_tag = post.get("primary_tag")
    time = get_current_time()
    if primary_tag["slug"] == "roundup":
        if html is not None and "kg-card" not in html:
            if previous is not None and "kg-card" not in previous["html"]:
                doc = generate_link_previews(post)
                LOGGER.info(f"Generated Previews for Lynx post {slug}: {doc}")
                body = {"posts": [{"mobiledoc": doc, "updated_at": time}]}
                response, code = ghost.update_post(post_id, body, slug)
                return make_response(f"Updated {slug} with code {code}: {doc}", 200)
        LOGGER.warning(f"Lynx post {slug} already contains previews.")
        return make_response(f"Lynx post {slug} already contains previews.", 422)


@LOGGER.catch
@api.route("/posts/update", methods=["GET"])
def post_metadata_sanitize():
    """Mass update post metadata."""
    queries = get_queries()
    results = db.execute_queries(queries, database_name="hackers_prod")
    headers = {"Content-Type": "application/json"}
    LOGGER.success(f"Successfully ran queries: {queries}")
    return make_response(jsonify(results), 200, headers)


@LOGGER.catch
@api.route("/posts/backup", methods=["GET"])
def backup_database():
    """Export JSON backup of database."""
    json = ghost.get_json_backup()
    return json
