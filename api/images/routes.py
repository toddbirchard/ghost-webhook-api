from flask import current_app as api
from flask import jsonify, make_response, request
import requests
from datetime import datetime
from api import ghst
from .fetch import fetch_recent_images, fetch_random_image
from .cleanup import clean_unwanted_images
from .transform import ImageTransformer
import json


transformer = ImageTransformer(api.config['GCP_BUCKET_NAME'],
                               api.config['GCP_BUCKET_URL'])


@api.route('/images/transform', methods=['GET'])
def transform_recent_images():
    """Apply image transformations to images in the current month."""
    retina_imgs, standard_imgs = fetch_recent_images(api.config['GCP_BUCKET_FOLDER'])
    clean_unwanted_images(retina_imgs, standard_imgs)
    retina_imgs, standard_imgs = fetch_recent_images(api.config['GCP_BUCKET_FOLDER'])
    response = transformer.bulk_transform_images(retina_from_standard=standard_imgs)
    return make_response(jsonify(response))


@api.route('/images/transform', methods=['POST'])
def transform_image():
    """Transform a single image upon post update."""
    data = request.get_json()
    fearured_image = data['post']['current'].get('feature_image')
    if fearured_image:
        response = transformer.transform_single_image(fearured_image)
    return make_response(jsonify(response))


@api.route('/images/lynx', methods=['POST'])
def set_lynx_image():
    post_id = request.get_json()['post']['current']['id']
    if 'lynx' in request.get_json()['post']['current']['title'].lower():
        token = ghst.get_session_token()
        image = fetch_random_image()
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
