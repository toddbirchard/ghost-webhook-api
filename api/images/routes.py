"""Routes to transform post images."""
from datetime import datetime
from flask import current_app as api
from flask import jsonify, make_response, request
import requests
from api import ghost, db
from api.log import LOGGER
from .fetch import fetch_image_blobs, fetch_random_lynx_image
from .transform import ImageTransformer


transformer = ImageTransformer(
    api.config['GCP_BUCKET_NAME'],
    api.config['GCP_BUCKET_URL']
)


@api.route('/images/transform', methods=['GET'])
def transform_recent_images():
    """Apply image transformations to images uploaded in the current month."""
    folder = request.args.get('directory', api.config['GCP_BUCKET_FOLDER'])
    retina_imgs, standard_imgs = fetch_image_blobs(folder)
    response = transformer.bulk_transform_images(folder, retina_from_standard=standard_imgs)
    LOGGER.info(f'Transformed images successfully: {response}')
    return make_response(jsonify(response))


@api.route('/images/transform/lynx', methods=['GET'])
def transform_lynx_images():
    """Apply image transformations to `Lynx` images."""
    folder = request.args.get('directory', 'roundup')
    retina_imgs, standard_imgs = fetch_image_blobs(folder)
    response = transformer.bulk_transform_images(folder, retina_from_standard=standard_imgs)
    LOGGER.info(f'Transformed images successfully: {response}')
    return make_response(jsonify(response))


@api.route('/images/transform', methods=['POST'])
def transform_image():
    """Transform single post image upon update."""
    post = request.get_json()['post']['current']
    featured_image = post.get('feature_image')
    title = post.get('title')
    if featured_image:
        response = transformer.transform_single_image(featured_image)
        LOGGER.info(f'Generated retina image for post `{title}`: {featured_image}')
        return make_response(jsonify(response))
    LOGGER.error(f'FAILED to generate retina image for post `{title}`: {featured_image}. {response}')
    return make_response(jsonify('FAILED'))


@api.route('/images/lynx', methods=['POST'])
def set_lynx_image():
    """Update single Lynx post with random image if `feature_image` is empty."""
    post = request.get_json()['post']['current']
    if post['primary_tag']['slug'] == 'roundup' and post['feature_image'] is None:
        token = ghost.get_session_token()
        image = fetch_random_lynx_image()
        body = {
            "posts": [{
                "feature_image": image,
                "updated_at": datetime.now().strftime("%Y-%m-%dT%I:%M:%S.000Z").replace(' ', '')
            }]
        }
        headers = {'Authorization': 'Ghost {}'.format(token.decode())}
        req = requests.put(
            f'{api.config["GHOST_API_BASE_URL"]}/posts/{post["id"]}/',
            json=body,
            headers=headers
        )
        if req.status_code == 200:
            LOGGER.info(f'Updated Lynx post `{post["feature_image"]}` with image {image}.')
            return make_response(jsonify({'SUCCESS': request.get_json()}))
        LOGGER.error(req.json())
        return make_response(jsonify({'FAILED': req.json()}))
    return make_response(request.get_json())


@api.route('/images/lynx', methods=['GET'])
def set_all_lynx_images():
    """Assign random image to Lynx posts which are missing a feature image."""
    sql = open('api/images/sql/lynx_missing_images.sql', 'r').read()
    results = db.execute_query(sql)
    posts = [result.id for result in results]
    for post in posts:
        image = fetch_random_lynx_image()
        db.update_post_image(image, post)
    LOGGER.info(f'Updated {len(posts)} lynx posts with images.')
    return make_response('Updated Lynx posts successfully.')
