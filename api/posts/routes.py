"""Routes to transform post data."""
import re
from datetime import datetime
from flask import current_app as api
from flask import jsonify, make_response
from .read import get_queries, read_sql_queries
from api import ghost, db
from api.log import LOGGER


@LOGGER.catch
@api.route('/posts/metadata', methods=['GET'])
def maintenance_queries():
    """Execute queries to optimize post posts."""
    queries = get_queries()
    results = db.execute_queries(queries)
    headers = {'Content-Type': 'application/json'}
    LOGGER.info(f'Successfully ran queries: {queries}')
    return make_response(jsonify(results), 200, headers)


@LOGGER.catch
@api.route('/posts/lynx', methods=['GET'])
def format_lynx_posts():
    """Replace <a> tags in Lynx posts."""
    updated_posts = []
    query = read_sql_queries(['api/posts/queries/lynx-bookmarks.sql'])
    results = db.fetch_records(query[0], table_name='blog')
    for result in results:
        links = re.findall('<a href="(.*?)"', result['html'])
        html = ''.join([f'<p><a href="{link}">{link}</a></p>' for link in links])
        post_id = result["id"]
        date = datetime.now().strftime("%Y-%m-%dT%I:%M:%S.000Z").replace(' ', '')
        post_body = {
            "posts": [{
                "html": html,
                "updated_at": date
            }]
        }
        updated_post = ghost.update_post(post_id, post_body)
        updated_posts.append(updated_post)
    headers = {'Content-Type': 'application/json'}
    return make_response(jsonify({'updated': updated_posts}), 200, headers)


@LOGGER.catch
@api.route('/posts/backup', methods=['GET'])
def backup_database():
    """Save JSON backup of database."""
    json = ghost.get_json_backup(api.config['GHOST_BASE_URL'], api.config['GHOST_API_KEY'])
    return json
