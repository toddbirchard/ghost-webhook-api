"""Routes to transform post data."""
from datetime import datetime
import requests
from flask import current_app as api
from flask import jsonify, make_response, request
from api import ghost, db
from api.log import LOGGER
from .read import get_queries
from .lynx.cards import format_lynx_posts


@LOGGER.catch
@api.route('/posts/metadata', methods=['GET'])
def maintenance_queries():
    """Execute SQL queries to fill missing post metadata."""
    queries = get_queries()
    results = db.execute_queries(queries)
    headers = {'Content-Type': 'application/json'}
    LOGGER.info(f'Successfully ran queries: {queries}')
    return make_response(jsonify(results), 200, headers)


@LOGGER.catch
@api.route('/posts/metadata', methods=['POST'])
def set_post_metadata():
    """Update post metadata where empty."""
    post = request.get_json()['post']['current']
    token = ghost.get_session_token()
    title = post.get('title')
    feature_image = post.get('feature_image')
    custom_excerpt = post.get('custom_excerpt')
    body = {
        "posts": [{
            "twitter_image": feature_image,
            "twitter_title": title,
            "twitter_description": custom_excerpt,
            "og_image": feature_image,
            "og_title": title,
            "og_description": custom_excerpt,
            "meta_title": title,
            "meta_description": custom_excerpt,
            "updated_at": datetime.now().strftime("%Y-%m-%dT%I:%M:%S.000Z").replace(' ', '')
            }]
    }
    headers = {'Authorization': token}
    req = requests.put(
        f'{api.config["GHOST_API_BASE_URL"]}/posts/{post["id"]}/',
        json=body,
        headers=headers
    )
    if req.status_code == 200:
        LOGGER.info(f'Updated post metadata for `{title}`: {req.json()}.')
        return make_response(jsonify({'SUCCESS': body}))
    LOGGER.error(f'request: {req.json()} response: {body}')
    return make_response(jsonify({'FAILED': req.json()}))


@LOGGER.catch
@api.route('/posts/metadata/lynx', methods=['POST'])
def set_lynx_metadata():
    """Replace <a> tags with embedded link previews."""
    post = request.get_json()['post']['current']
    token = ghost.get_session_token()
    primary_tag = post.get('primary_tag')
    if primary_tag.get('slug') == 'roundup':
        doc = format_lynx_posts(post)
        body = {
            "posts": [{
                "mobiledoc": doc,
                "updated_at": datetime.now().strftime("%Y-%m-%dT%I:%M:%S.000Z").replace(' ', '')
            }]
        }
        headers = {'Authorization': token}
        req = requests.put(
            f'{api.config["GHOST_API_BASE_URL"]}/posts/{post["id"]}/',
            json=body,
            headers=headers
        )
        if req.status_code == 200:
            LOGGER.info(f'Updated lynx: {req.json()}.')
            return make_response(jsonify({'SUCCESS': body}))
        LOGGER.error(f'request: {req.json()} response: {body}')
        return make_response(jsonify({'FAILED': req.json()}))
    return make_response(jsonify({'RESULT': 'Ignored non-lynx post.'}), 204)


@LOGGER.catch
@api.route('/posts/backup', methods=['GET'])
def backup_database():
    """Save JSON backup of database."""
    json = ghost.get_json_backup()
    return json
