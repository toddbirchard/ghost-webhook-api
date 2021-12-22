"""Generate optimized images to be served from Google Cloud CDN."""
from typing import Optional

from fastapi import APIRouter, Query
from fastapi.responses import PlainTextResponse

from clients import gcs
from config import BASE_DIR, settings
from database import rdbms
from database.schemas import PostUpdate
from log import LOGGER

router = APIRouter(prefix="/images", tags=["images"])


@router.post(
    "/",
    summary="Optimize single post image.",
    description="Generate retina and mobile feature_image for a single post upon update.",
)
async def optimize_post_image(post_update: PostUpdate):
    """
    Generate retina version of a post's feature image if one doesn't exist.

    :param post_update: Incoming payload for an updated Ghost post.
    :type post_update: PostUpdate
    """
    new_images = []
    post = post_update.post.current
    feature_image = post.feature_image
    title = post.title
    if feature_image:
        new_images.append(gcs.create_retina_image(feature_image))
        new_images.append(gcs.create_mobile_image(feature_image))
        new_images = [image for image in new_images if image is not None]
        if bool(new_images):
            LOGGER.info(
                f"Generated {len(new_images)} images for post `{title}`: {new_images}"
            )
            return {post.title: new_images}
        return PlainTextResponse(
            content=f"Retina & mobile images already exist for {post.title}."
        )
    return PlainTextResponse(
        content=f"Post `{post.slug}` ignored; no image exists for optimization."
    )


@router.get(
    "/",
    summary="Batch optimize CDN images.",
    description="Generates retina and mobile varieties of post feature_images. \
            Defaults to images uploaded within the current month; \
            accepts a `?directory=` parameter which accepts a path to recursively optimize images on the given CDN.",
)
async def bulk_transform_images(
    directory: Optional[str] = Query(
        default=None,
        title="directory",
        description="Subdirectory of remote CDN to transverse and transform images.",
        max_length=50,
    )
):
    """
    Apply transformations to images uploaded within the current month.
    Optionally accepts a `directory` parameter to override image directory.

    :param directory: Remote directory to recursively fetch images and apply transformations.
    :type directory: Optional[str]
    """
    if directory is None:
        directory = settings.GCP_BUCKET_FOLDER
    images = {
        "purged": gcs.purge_unwanted_images(directory),
        "retina": gcs.retina_transformations(directory),
        "mobile": gcs.mobile_transformations(directory),
        # "standard": gcs.standard_transformations(directory),
    }
    log = []
    for k, v in images.items():
        if v is not None:
            log.append(f"{len(v)} {k}")
        else:
            log.append(f"0 {k}")
    LOGGER.success(f"Transformed {', '.join(log)} images")
    return images


@router.get("/lynx")
async def bulk_assign_lynx_images():
    """Assign images to any Lynx posts which are missing a feature image."""
    results = rdbms.execute_query_from_file(
        f"{BASE_DIR}/database/queries/images/lynx_missing_images.sql", "hackers_dev"
    )
    posts = [result.id for result in results]
    for post in posts:
        image = gcs.fetch_random_lynx_image()
        result = rdbms.execute_query(
            f"UPDATE posts SET feature_image = '{image}' WHERE id = '{post}';",
            "hackers_dev",
        )
        if result:
            LOGGER.info(f"Updated Lynx post {post} with image {image}")
    LOGGER.success(f"Updated {len(posts)} Lynx posts with image")
    return {"updated": posts}


@router.get("/sort")
async def bulk_organize_images(directory: Optional[str] = None):
    """
    Sort retina and mobile images into their appropriate directories.

    :param directory: Remote directory to organize images into subdirectories.
    :type directory: Optional[str]
    """
    if directory is None:
        directory = settings.GCP_BUCKET_FOLDER
    retina_images = gcs.organize_retina_images(directory)
    image_headers = gcs.image_headers(directory)
    LOGGER.success(
        f"Moved {len(retina_images)} retina images, modified {len(image_headers)} content types."
    )
    return {
        "retina": retina_images,
        "headers": image_headers,
    }
