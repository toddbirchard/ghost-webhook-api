"""Routes to transform post data."""
from datetime import datetime, timedelta
from flask import current_app as api
from flask import jsonify, make_response, request
from api import ghost, db, image
from api.log import LOGGER
from .read import get_queries
from .lynx.cards import format_lynx_posts


@LOGGER.catch
@api.route('/post/update', methods=['POST'])
def set_post_metadata():
    """Update post metadata where empty."""
    post = request.get_json()['post']['current']
    id = post.get('id')
    title = post.get('title')
    feature_image = post.get('feature_image', None)
    custom_excerpt = post.get('custom_excerpt')
    primary_tag = post.get('primary_tag')
    body = {
        "posts": [{
            "meta_title": title,
            "og_title": title,
            "twitter_title": title,
            "meta_description": custom_excerpt,
            "twitter_description": custom_excerpt,
            "og_description": custom_excerpt,
            "updated_at": (datetime.now() + timedelta(seconds=1)).strftime("%Y-%m-%dT%I:%M:%S.000Z").replace(' ', '')
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
    elif feature_image is not None and '@2x' not in feature_image:
        # Create retina image for new post
        feature_image = image.transform_single_image(feature_image)
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
    LOGGER.info('feature_image = ', feature_image)
    response = ghost.update_post(id, body)
    return make_response(jsonify(response))


@LOGGER.catch
@api.route('/post/lynx', methods=['POST'])
def set_lynx_metadata():
    """Replace <a> tags with embedded link previews."""
    post = request.get_json()['post']['current']
    id = post.get('id')
    primary_tag = post.get('primary_tag')
    if primary_tag.get('slug') == 'roundup':
        doc = format_lynx_posts(post)
        body = {
            "posts": [{
                "mobiledoc": doc,
                "updated_at": datetime.now().strftime("%Y-%m-%dT%I:%M:%S.000Z").replace(' ', '')
            }]
        }
        response = ghost.update_post(id, body)
        return make_response(jsonify(response))
    else:
        return make_response(jsonify({'IGNORED': 'Non-lynx post.'}), 204)


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
