from api import db
from .fetch import fetch_random_image


def update_post_image(post_id):
    image = fetch_random_image()
    sql = f"UPDATE posts SET feature_image = '{image}' WHERE id = '{post_id}';"
    db.execute_query(sql)
    return {post_id: image.split('/')[-1]}
