"""Routes to transform post data."""
from flask import current_app as api
from flask import jsonify, make_response, request
from api import ghost, db, image
from api.log import LOGGER
from api.moment import get_current_time
from .read import get_queries
from .lynx.cards import format_lynx_posts


@LOGGER.catch
@api.route('/post/update', methods=['POST'])
def set_post_metadata():
    """Update post metadata where empty."""
    post = request.get_json()['post']['current']
    id = post.get('id')
    slug = post.get('slug')
    title = post.get('title')
    feature_image = post.get('feature_image')
    custom_excerpt = post.get('custom_excerpt')
    primary_tag = post.get('primary_tag')
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
    if feature_image is None and primary_tag.get('slug') == 'roundup':
        # Assign random image to new Lynx post
        feature_image = image.fetch_random_lynx_image()
        body['posts'][0].update({
            "feature_image": feature_image,
            "og_image": feature_image,
            "twitter_image": feature_image
        })
    elif feature_image is not None:
        # Sync social images with feature image
        body['posts'][0].update({
            "og_image": feature_image,
            "twitter_image": feature_image
        })
    response, code = ghost.update_post(id, body, slug)
    return make_response(jsonify(response), code)


@LOGGER.catch
@api.route('/post/lynx/previews', methods=['POST'])
def set_lynx_metadata():
    """Replace <a> tags with embedded link previews."""
    post = request.get_json()['post']['current']
    id = post.get('id')
    slug = post.get('slug')
    primary_tag = post.get('primary_tag')
    time = get_current_time()
    if primary_tag.get('slug') == 'roundup':
        doc = format_lynx_posts(post)
        body = {
            "posts": [{
                "mobiledoc": doc,
                "updated_at": time
            }]
        }
        response, code = ghost.update_post(id, body, slug)
        return make_response(jsonify(response), code)


@LOGGER.catch
@api.route('/post/metadata', methods=['GET'])
def maintenance_queries():
    """Execute SQL queries to fill missing post metadata."""
    queries = get_queries()
    results = db.execute_queries(queries)
    headers = {'Content-Type': 'application/json'}
    LOGGER.info(f'Successfully ran queries: {queries}')
    return make_response(jsonify(results), 200, headers)


@LOGGER.catch
@api.route('/post/backup', methods=['GET'])
def backup_database():
    """Save JSON backup of database."""
    json = ghost.get_json_backup()
    return json
