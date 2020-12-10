import re
from typing import List, Optional

from clients import ghost
from config import basedir
from database import rdbms


def assign_alt_text_to_imgs():
    total_images = []
    updated_posts = []
    posts = posts_missing_alt_text()
    for post in posts:
        images = extract_image_cards(post)
        image_cards = generate_img_tags(images)
        total_images.append(image_cards)
        updated_html = update_post_html(post, image_cards)
        if updated_html:
            post_update = update_post_images(post, updated_html)
            if post_update:
                updated_posts.append(
                    {
                        post["slug"]: {
                            "count": len(total_images),
                            "images": total_images,
                        }
                    }
                )
            return {
                "summary": {
                    "total_posts": len(posts),
                    "updated_posts": len(updated_posts),
                },
                "posts": updated_posts,
            }


def posts_missing_alt_text() -> Optional[List[str]]:
    sql_query = f"{basedir}/database/queries/posts/selects/img_alt_missing.sql"
    posts = rdbms.execute_query_from_file(sql_query, "hackers_prod")
    return [ghost.get_post(post["id"]) for post in posts]


def extract_image_cards(post):
    fixable_images = []
    post_html = post["html"]
    image_matcher = '(?<=<figure class=\\"kg-card kg-image-card kg-card-hascaption\\").*?(?=<\\/figure>)'
    images = re.findall(image_matcher, post_html)
    images = filter(lambda x: "<a href" not in x, images)
    fixable_images.extend(images)
    return fixable_images


def generate_img_tags(images) -> List[dict]:
    captions_per_post = []
    for image in images:
        img_tag = re.search("<img.*?(?=>)>", image).group()
        caption = re.search("(?<=<figcaption>).*?(?=</figcaption>)", image).group()
        if caption:
            img_src = re.search('(?<=src=").*?(?=\\")', image).group()
            img_tag_new = f'<a data-srcset="{img_src}" alt="{caption}" title="{caption}" class="kg-image lazyload"/>'
            captions_per_post.append(
                {
                    "img_src": img_src,
                    "caption": caption,
                    "img_tag": img_tag,
                    "img_tag_new": img_tag_new,
                }
            )
    return captions_per_post


def update_post_html(post: dict, images: List[dict]) -> Optional[str]:
    new_post_html = post["html"]
    for image in images:
        new_post_html = new_post_html.replace(image["img_tag"], image["img_tag_new"])
    if new_post_html != post["html"]:
        return new_post_html
    return None


def update_post_images(post: dict, html: str):
    body = {
        "posts": [
            {
                "html": html,
                "updated_at": post["updated_at"],
            }
        ]
    }
    response, status_code = ghost.update_post(post["id"], body, post["slug"])
    if status_code == 200:
        return True
