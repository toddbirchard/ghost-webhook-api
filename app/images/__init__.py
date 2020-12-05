"""Generate optimized images to be served from Google Cloud CDN."""
from typing import Optional

from fastapi import APIRouter

from clients import gcs
from clients.log import LOGGER
from config import Settings
from database import rdbms

from .models import PostUpdate

router = APIRouter(prefix="/images", tags=["images"])


@router.post(
    "/post",
    summary="Optimize post image.",
    description="Generate retina and mobile feature_image for a single post upon update.",
)
def optimize_post_image(post_update: PostUpdate):
    """Generate retina version of a post's feature image if one doesn't exist."""
    post = post_update.post.current
    feature_image = post.feature_image
    title = post.title
    retina_image = gcs.create_single_retina_image(feature_image)
    mobile_image = gcs.create_single_mobile_image(feature_image)
    new_images = filter(lambda x: x is not None, [retina_image, mobile_image])
    LOGGER.info(f"Generated images for post `{title}`: {', '.join(new_images)}")
    return {"retina": retina_image, "mobile": mobile_image}


@router.get(
    "/transform",
    summary="Run batch optimizations on images.",
    description="Generate retina and mobile feature image for a single post upon update.",
)
def bulk_transform_images(directory: Optional[str] = None):
    """
    Apply transformations to images uploaded within the current month.
    Optionally accepts a `directory` parameter to override image directory.
    """
    if directory is None:
        directory = Settings().GCP_BUCKET_FOLDER
    purged_images = gcs.purge_unwanted_images(directory)
    retina_images = gcs.retina_transformations(directory)
    mobile_images = gcs.mobile_transformations(directory)
    standard_images = gcs.standard_transformations(directory)
    LOGGER.success(
        f"Transformed {len(mobile_images)} mobile, {len(retina_images)} retina, {len(standard_images)} standard images."
    )
    return {
        "purged": purged_images,
        "retina": retina_images,
        "mobile": mobile_images,
        "standard": standard_images,
    }


@router.get("/purge")
def purge_images(directory: Optional[str] = None):
    """Purge unwanted images."""
    if directory is None:
        directory = Settings().GCP_BUCKET_FOLDER
    purged_images = gcs.purge_unwanted_images(directory)
    LOGGER.success(f"Deleted {purged_images} unwanted images")
    return {"purged": purged_images}


@router.get("/lynx")
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
            LOGGER.info(f"Updated Lynx post {post} with image {image}")
    LOGGER.success(f"Updated {len(posts)} Lynx posts with image")
    return {"updated": posts}


@router.get("/sort")
def bulk_organize_images(directory: Optional[str] = None):
    """"""
    if directory is None:
        directory = Settings().GCP_BUCKET_FOLDER
    retina_images = gcs.organize_retina_images(directory)
    image_headers = gcs.image_headers(directory)
    LOGGER.success(
        f"Moved {len(retina_images)} retina images, modified {len(image_headers)} content types."
    )
    return {
        "retina": retina_images,
        "headers": image_headers,
    }
