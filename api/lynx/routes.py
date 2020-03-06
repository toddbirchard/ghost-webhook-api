from flask import current_app as api
from flask import make_response, request, jsonify
import requests
from datetime import datetime
from .fetch import get_random_image
from .auth import get_session_token


@api.route('/lynx', methods=['POST'])
def set_lynx_image():
    token = get_session_token()
    image = get_random_image()
    post_id = request.get_json()['post']['current']['id']
    if 'lynx' in request.get_json()['post']['current']['title'].lower():
        body = {
            "posts": [{
                "feature_image": image,
                "updated_at": datetime.now().strftime("%Y-%m-%dT%I:%M:%S.000Z").replace(' ', '')
            }]
        }
        headers = {'Authorization': 'Ghost {}'.format(token.decode())}
        r = requests.put(f'{api.config["GHOST_API_BASE_URL"]}/posts/{post_id}/',
                         json=body,
                         headers=headers)
        if r.status_code == 200:
            return make_response(jsonify({'SUCCESS': request.get_json()}))
        return make_response(jsonify({'FAILED': r.json()}))
    return make_response(request.get_json())
