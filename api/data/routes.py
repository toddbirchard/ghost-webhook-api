from flask import current_app as api
from flask import jsonify, make_response
import requests
from .read import get_queries
from api import ghost, db


@api.route('/metadata', methods=['GET'])
def maintenance_queries():
    """Execute queries to optimize post data."""
    queries = get_queries()
    results = db.run_query(queries)
    headers = {'Content-Type': 'application/json'}
    return make_response(jsonify(results), 200, headers)


@api.route('/backup', methods=['GET'])
def backup_database():
    """Save JSON backup of database."""
    token = ghost.get_session_token()
    headers = {'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
               'accept-encoding': 'gzip, deflate, br',
               'Authorization': 'Ghost {}'.format(token.decode())}
    endpoint = f'{api.config["GHOST_BASE_URL"]}/ghost/api/v3/admin/db/'
    backup_json = requests.get(endpoint, headers=headers)
    print(backup_json)
    return backup_json.json()
