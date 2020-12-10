from typing import List, Optional
import re
from config import basedir
from database import rdbms
from clients import ghost
from clients.log import LOGGER


def posts_missing_alt_text() -> Optional[List[str]]:
    sql_query = f"{basedir}/database/queries/posts/selects/img_alt_missing.sql"
    posts = rdbms.execute_query_from_file(sql_query, "hackers_prod")
    return [ghost.get_post(post['id']) for post in posts]


def extract_image_cards():
    fixed_images = []
    posts = posts_missing_alt_text()
    for post in posts:
        post_html = post['html']
        image_matcher = '(?<=<figure class=\\"kg-card kg-image-card kg-card-hascaption\\").*?(?=<\\/figure>)'
        images = re.findall(image_matcher, post_html)
        images = filter(lambda x: "<a href" not in x, images)
        if bool(images):
            captions_per_post = []
            for image in images:
                caption = re.search(
                    "(?<=<figcaption>).*?(?=</figcaption>)", image
                ).group()
                result, status_code = update_post_images(post_html)
                if status_code == 200:
                    captions_per_post.append(caption)
    return fixed_images


def update_post_images(html: str):
    posts = extract_image_cards()
    for post in posts:
        body = {
            "posts": [
                {
                    "html": html,
                    "updated_at": post["updated_at"],
                }
            ]
        }
        return ghost.update_post(post["id"], body, post["slug"])
