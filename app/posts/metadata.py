"""Execute SQL to ensure posts have properly optimized metadata."""

from typing import Tuple

from app.posts.update import bulk_update_post_metadata
from config import settings
from database import ghost_db
from database.read_sql import collect_sql_queries
from log import LOGGER


def optimize_posts_metadata() -> Tuple[int, int]:
    """
    Bulk optimize metadata for blog posts with incorrect or missing data.

    :returns: Tuple[int, int]
    """
    post_update_queries = collect_sql_queries("posts/updates")
    posts_metadata_updated = update_posts_metadata(post_update_queries)
    posts_metadata_added = insert_posts_metadata()
    return posts_metadata_updated, posts_metadata_added


def update_posts_metadata(post_update_queries: dict) -> int:
    """
    Update posts with mismatched metadata.

    :param dict post_update_queries: Queries to update posts with mismatched metadata.

    :returns: int
    """
    update_results = ghost_db.execute_queries(post_update_queries)
    if update_results:
        LOGGER.success(f"Updated metadata for {len(update_results)} posts.")
        return len(update_results)
    return 0


def insert_posts_metadata() -> int:
    """
    Insert metadata for all posts which are missing fields.

    :returns: int
    """
    insert_posts = ghost_db.execute_query_from_file(
        f"{settings.BASE_DIR}/database/queries/posts/selects/missing_all_metadata.sql",
    )
    insert_results = bulk_update_post_metadata(insert_posts)
    if insert_results:
        LOGGER.success(f"Inserted metadata for {len(insert_results)} posts.")
        return insert_results
    return 0
