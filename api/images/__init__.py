"""Generate and export optimized images."""
from flask import current_app as api
from flask import jsonify, make_response, request

from clients import db, gcs
from clients.log import LOGGER

headers = {"content-type": "application/json"}


@LOGGER.catch
@api.route("/images/post", methods=["POST"])
def create_post_retina_image():
    """Generate retina version of a post's feature image if one doesn't exist."""
    post = request.get_json()["post"]["current"]
    feature_image = post.get("feature_image")
    title = post.get("title")
    if feature_image is not None and "@2x" not in feature_image:
        new_image = gcs.create_single_retina_image(feature_image)
        LOGGER.success(f"Created image for post `{title}`: {new_image}")
        return make_response(jsonify({title: new_image}), 200, headers)
    return make_response(
        f"Post `{post}` already has retina image {feature_image}", 422, headers
    )


@api.route("/images/transform", methods=["GET"])
def transform_images():
    """
    Apply transformations to images uploaded within the current month.
    Optionally accepts a `directory` parameter to override image directory.
    """
    folder = request.args.get("directory", api.config["GCP_BUCKET_FOLDER"])
    purged_images = gcs.purge_unwanted_images(folder)
    mobile_images = gcs.mobile_transformations(folder)
    retina_images = gcs.retina_transformations(folder)
    LOGGER.success(
        f"Transformed {len(mobile_images)} mobile, {len(retina_images)} retina images."
    )
    return make_response(
        jsonify(
            {"purged": purged_images, "retina": retina_images, "mobile": mobile_images}
        ),
        200,
        headers,
    )


@api.route("/images/purge", methods=["GET"])
def purge_images():
    """Purge unwanted images."""
    folder = request.args.get("directory", api.config["GCP_BUCKET_FOLDER"])
    purged_images = gcs.purge_unwanted_images(folder)
    LOGGER.success(f"Deleted {purged_images} unwanted images.")
    return make_response(jsonify({"purged": purged_images}), 200, headers)


@api.route("/images/mobile", methods=["GET"])
def transform_mobile_images():
    """Apply transformations to image uploaded within the current month."""
    folder = request.args.get("directory", api.config["GCP_BUCKET_FOLDER"])
    purged_images = gcs.purge_unwanted_images(folder)
    mobile_images = gcs.mobile_transformations(folder)
    LOGGER.success(f"Transformed {len(mobile_images)} mobile image(s).")
    return make_response(
        jsonify({"purged": purged_images, "mobile": mobile_images}), 200, headers
    )


@api.route("/images/lynx", methods=["GET"])
def assign_lynx_images():
    """Assign images to any Lynx posts which are missing a feature image."""
    results = db.execute_query_from_file(
        "api/images/sql/lynx_missing_images.sql", database_name="hackers_prod"
    )
    posts = [result.id for result in results]
    for post in posts:
        image = gcs.fetch_random_lynx_image()
        db.execute_query(
            f"UPDATE posts SET feature_image = '{image}' WHERE id = '{post}';",
            database_name="hackers_prod",
        )
    LOGGER.success(f"Updated {len(posts)} lynx posts with image.")
    return make_response(jsonify({"updated": posts}), 200, headers)


@api.route("/images/move", methods=["GET"])
def organize_images():
    folder = request.args.get("directory", api.config["GCP_BUCKET_FOLDER"])
    moved_images = gcs.organize_retina_images(folder)
    image_headers = gcs.image_headers(folder)
    moved_mobile_images = gcs.organize_mobile_images(folder)
    LOGGER.success(
        f"Moved {len(moved_images)} mobile & {len(moved_mobile_images)} mobile images."
    )
    return make_response(
        jsonify(
            {
                "mobile": moved_images,
                "retina": moved_mobile_images,
                "headers": image_headers,
            }
        ),
        200,
        headers,
    )


@api.route("/images/headers", methods=["GET"])
def organize_images_headers():
    folder = request.args.get("directory", api.config["GCP_BUCKET_FOLDER"])
    headers_images = gcs.image_headers(folder)
    LOGGER.success(f"Modified {len(headers_images)} images.")
    return make_response(jsonify({"headers": headers_images}), 200, headers)
