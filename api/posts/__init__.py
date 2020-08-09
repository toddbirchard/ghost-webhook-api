"""Routes to transform post data."""
from time import sleep
from flask import current_app as api
from flask import jsonify, make_response, request
from api import db, image
from api.log import LOGGER
from api.moment import get_current_time
from api import ghost
from .read import get_queries
from .lynx.cards import generate_link_previews


@LOGGER.catch
@api.route('/posts/update', methods=['POST'])
def update_post():
    """Update post metadata & render Lynx previews."""
    post = request.get_json()['post']['current']
    post_id = post.get('id')
    slug = post.get('slug')
    title = post.get('title')
    feature_image = post.get('feature_image')
    custom_excerpt = post.get('custom_excerpt')
    primary_tag = post.get('primary_tag')
    html = post.get('html')
    previous = post.get('previous')
    time = get_current_time()
    body = {
        "posts": [{
            "meta_title": title,
            "og_title": title,
            "twitter_title": title,
            "meta_description": custom_excerpt,
            "twitter_description": custom_excerpt,
            "og_description": custom_excerpt,
            "updated_at": time
            }
        ]
    }
    if primary_tag.get('slug') == 'roundup':
        if feature_image is None:
            feature_image = image.fetch_random_lynx_image()
            body['posts'][0].update({
                "feature_image": feature_image,
                "og_image": feature_image,
                "twitter_image": feature_image
             })
        if 'kg-card' not in html or 'kg-card' not in previous['html']:
            doc = generate_link_previews(post)
            LOGGER.info(f'Generated Previews for Lynx post {slug}.')
            # body['posts'][0].update({
            #     "mobiledoc": doc
            # })
    # Update image meta tags
    elif feature_image is not None:
        body['posts'][0].update({
            "og_image": feature_image,
            "twitter_image": feature_image
        })
    if body['posts'][0].get('mobiledoc'):
        sleep(1)
        time = get_current_time()
        body['posts'][0]['updated_at'] = time
    LOGGER.info(f'Originally updated at {post.get("updated_at")}, new timestamp {time}')
    response, code = ghost.update_post(post_id, body, slug)
    LOGGER.info(f'Post Updated with code {code}: {body}')
    return make_response(response, code)


@LOGGER.catch
@api.route('/posts/embed', methods=['POST'])
def generate_embedded_link_previews():
    """Render Lynx previews."""
    post = request.get_json()['post']['current']
    post_id = post.get('id')
    slug = post.get('slug')
    html = post.get('html')
    previous = post.get('previous')
    primary_tag = post.get('primary_tag')
    time = get_current_time()
    if primary_tag['slug'] == 'roundup':
        if 'kg-card' not in html or 'kg-card' not in previous['html']:
            doc = generate_link_previews(post)
            LOGGER.info(f'Generated Previews for Lynx post {slug}: {doc}')
            body = {
                "posts": [{
                    "mobiledoc": doc,
                    "updated_at": time
                }
                ]
            }
            response, code = ghost.update_post(post_id, body, slug)
            # db.execute_query(f"UPDATE posts SET mobiledoc = '{doc}' WHERE id = '{post_id}';")
            return make_response(f'Updated {slug} with code {code}: {doc}', 200)
        return make_response(f'Lynx post {slug} already contains previews.', 200)
    pass
    

@LOGGER.catch
@api.route('/posts/metadata', methods=['GET'])
def post_metadata_sanitize():
    """Mass update post metadata."""
    queries = get_queries()
    results = db.execute_queries(queries)
    headers = {'Content-Type': 'application/json'}
    LOGGER.info(f'Successfully ran queries: {queries}')
    return make_response(jsonify(results), 200, headers)


@LOGGER.catch
@api.route('/posts/backup', methods=['GET'])
def backup_database():
    """Save JSON backup of database."""
    json = ghost.get_json_backup()
    return json
