from flask import current_app as api
from flask import jsonify, make_response
from .read import get_queries
from api import ghost, db
from api.log import logger


@logger.catch
@api.route('/data/posts', methods=['GET'])
def maintenance_queries():
    """Execute queries to optimize post data."""
    queries = get_queries()
    results = db.execute_queries(queries)
    headers = {'Content-Type': 'application/json'}
    return make_response(jsonify(results), 200, headers)


@logger.catch
@api.route('/data/backup', methods=['GET'])
def backup_database():
    """Save JSON backup of database."""
    json = ghost.get_json_backup(api.config['GHOST_BASE_URL'], api.config['GHOST_API_KEY'])
    return json
