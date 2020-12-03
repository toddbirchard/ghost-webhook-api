"""Generate optimized images to be served from Google Cloud CDN."""
from flask import current_app as api
from flask import jsonify, make_response, request

from clients import gcs
from clients.log import LOGGER
from database import rdbms

headers = {"content-type": "application/json"}


@LOGGER.catch
@api.route("/images/post", methods=["POST"])
def optimize_post_image():
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
def bulk_transform_images():
    """
    Apply transformations to images uploaded within the current month.
    Optionally accepts a `directory` parameter to override image directory.
    """
    folder = request.args.get("directory", api.config["GCP_BUCKET_FOLDER"])
    purged_images = gcs.purge_unwanted_images(folder)
    retina_images = gcs.retina_transformations(folder)
    mobile_images = gcs.mobile_transformations(folder)
    standard_images = gcs.standard_transformations(folder)
    LOGGER.success(
        f"Transformed {len(mobile_images)} mobile, {len(retina_images)} retina, {len(standard_images)} standard images."
    )
    return make_response(
        jsonify(
            {
                "purged": purged_images,
                "retina": retina_images,
                "mobile": mobile_images,
                "standard": standard_images,
            }
        ),
        200,
        headers,
    )


@api.route("/images/transform/retina", methods=["GET"])
def bulk_transform_retina_images():
    """Apply retina transformations to image uploaded within the current month."""
    folder = request.args.get("directory", api.config["GCP_BUCKET_FOLDER"])
    purged_images = gcs.purge_unwanted_images(folder)
    retina_images = gcs.retina_transformations(folder)
    LOGGER.success(f"Transformed {len(retina_images)} retina image(s).")
    return make_response(
        jsonify({"purged": purged_images, "mobile": retina_images}), 200, headers
    )


@api.route("/images/transform/mobile", methods=["GET"])
def bulk_transform_mobile_images():
    """Apply mobile transformations to image uploaded within the current month."""
    folder = request.args.get("directory", api.config["GCP_BUCKET_FOLDER"])
    purged_images = gcs.purge_unwanted_images(folder)
    mobile_images = gcs.mobile_transformations(folder)
    LOGGER.success(f"Transformed {len(mobile_images)} mobile image(s).")
    return make_response(
        jsonify({"purged": purged_images, "mobile": mobile_images}), 200, headers
    )


@api.route("/images/purge", methods=["GET"])
def purge_images():
    """Purge unwanted images."""
    folder = request.args.get("directory", api.config["GCP_BUCKET_FOLDER"])
    purged_images = gcs.purge_unwanted_images(folder)
    LOGGER.success(f"Deleted {purged_images} unwanted images.")
    return make_response(jsonify({"purged": purged_images}), 200, headers)


@api.route("/images/lynx", methods=["GET"])
def bulk_assign_lynx_images():
    """Assign images to any Lynx posts which are missing a feature image."""
    results = rdbms.execute_query_from_file(
        "app/images/sql/lynx_missing_images.sql", "hackers_prod"
    )
    posts = [result.id for result in results]
    for post in posts:
        image = gcs.fetch_random_lynx_image()
        result = rdbms.execute_query(
            f"UPDATE posts SET feature_image = '{image}' WHERE id = '{post}';",
            "hackers_prod",
        )
        if result:
            LOGGER.info(f"Updated lynx post {post} with image {image}")
    LOGGER.success(f"Updated {len(posts)} lynx posts with image.")
    return make_response(jsonify({"updated": posts}), 200, headers)


@api.route("/images/sort", methods=["GET"])
def bulk_organize_images():
    folder = request.args.get("directory", api.config["GCP_BUCKET_FOLDER"])
    retina_images = gcs.organize_retina_images(folder)
    image_headers = gcs.image_headers(folder)
    LOGGER.success(
        f"Moved {len(retina_images)} retina images and modified {len(image_headers)} content-types."
    )
    return make_response(
        jsonify(
            {
                "retina": retina_images,
                "headers": image_headers,
            }
        ),
        200,
        headers,
    )
