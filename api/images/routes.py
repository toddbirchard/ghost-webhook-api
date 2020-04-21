from flask import current_app as api
from flask import jsonify, make_response, request
import requests
from datetime import datetime
from api import ghost, gcs
from .fetch import fetch_recent_images, fetch_random_image
from .transform import ImageTransformer
from .update import update_post
from api import gbq, db
from loguru import logger


transformer = ImageTransformer(api.config['GCP_BUCKET_NAME'],
                               api.config['GCP_BUCKET_URL'])

logger.add("logs/errors.log", colorize=True, rotation="500 MB", format="<green>{time}</green> <level>{message}</level>")


@api.route('/images/transform', methods=['GET'])
def transform_recent_images():
    """Apply image transformations to images in the current month."""
    folder = request.args['prefix'] if request.args.get('prefix', None) else api.config['GCP_BUCKET_FOLDER']
    substrings = ['@2x@2x', '_o']
    images = gcs.get(folder)
    gcs.purge_images(substrings, images)
    retina_imgs, standard_imgs = fetch_recent_images(folder)
    response = transformer.bulk_transform_images(retina_from_standard=standard_imgs)
    return make_response(jsonify(response))


@logger.catch
@api.route('/images/transform', methods=['POST'])
def transform_image():
    """Transform a single image upon post update."""
    data = request.get_json()
    featured_image = data['post']['current'].get('feature_image')
    if featured_image:
        response = transformer.transform_single_image(featured_image)
        return make_response(jsonify(response))
    return make_response(jsonify('FAILED'))


@api.route('/images/lynx', methods=['POST'])
def set_lynx_image():
    post = request.get_json()['post']['current']['id']
    if 'roundup' in post['tags'][0]['slug'].lower() and post['feature_image'] is None:
        token = ghost.get_session_token()
        image = fetch_random_image()
        body = {
            "posts": [{
                "feature_image": image,
                "updated_at": datetime.now().strftime("%Y-%m-%dT%I:%M:%S.000Z").replace(' ', '')
            }]
        }
        headers = {'Authorization': 'Ghost {}'.format(token.decode())}
        r = requests.put(f'{api.config["GHOST_API_BASE_URL"]}/posts/{post["id"]}/',
                         json=body,
                         headers=headers)
        if r.status_code == 200:
            return make_response(jsonify({'SUCCESS': request.get_json()}))
        else:
            logger.error(r.json())
            return make_response(jsonify({'FAILED': r.json()}))
    return make_response(request.get_json())


@api.route('/images/lynx/all', methods=['GET'])
def set_all_lynx_images():
    """Update all missing Lynx feature images."""
    updated = []
    results = db.execute_query("SELECT id FROM posts WHERE title LIKE '%%lynx%%' AND feature_image IS NULL;")
    posts = [result[0] for result in results]
    for post_id in posts:
        updated.append(update_post(post_id))
    return make_response(jsonify({'UPDATED': updated}))
