"""Routes to transform post images."""
from flask import current_app as api
from flask import jsonify, make_response, request
from api import db, image
from api.log import LOGGER


@LOGGER.catch
@api.route('/image/transform', methods=['POST'])
def create_post_retina_image():
    """Create retina image on post update."""
    post = request.get_json()['post']['current']
    feature_image = post.get('feature_image')
    title = post.get('title')
    if feature_image is not None and '@2x' not in feature_image:
        LOGGER.info(f'Creating images for updated post {title}.')
        new_image = image.create_single_retina_image(feature_image)
        return make_response(jsonify({title: new_image}))


@api.route('/images/transform', methods=['GET'])
def transform_recent_images():
    """Apply transformations to images uploaded within the current month."""
    folder = request.args.get('directory', api.config['GCP_BUCKET_FOLDER'])
    retina_images = image.fetch_image_blobs(folder, 'retina')
    standard_images = image.fetch_image_blobs(folder, 'standard')
    LOGGER.info(f'Checking {len(retina_images)} retina and {len(standard_images)} standard images in {folder}')
    standard, retina, webp = image.bulk_transform_images(folder, standard_images, retina_images)
    response = {'retina': retina, 'standard': standard, 'webp': webp}
    LOGGER.info(f'Transformed images successfully: {response}')
    return make_response(jsonify(response))


@api.route('/images/transform/lynx', methods=['GET'])
def transform_lynx_images():
    """Apply transformations to all `Lynx` images."""
    folder = 'roundup'
    lynx_images = image.fetch_image_blobs(folder)
    response = image.bulk_transform_images(folder, lynx_images, transformation='retina')
    LOGGER.info(f'Transformed {response} images successfully!')
    return make_response(jsonify({'SUCCESS': f'Transformed {response} images successfully!'}))


@api.route('/images/assign/lynx', methods=['GET'])
def assign_missing_lynx_images():
    """Assign random image to Lynx posts which are missing a feature image."""
    results = db.execute_query_from_file('api/images/sql/lynx_missing_images.sql')
    posts = [result.id for result in results]
    for post in posts:
        new_feature_image = image.fetch_random_lynx_image()
        db.update_post_image(new_feature_image, post)
    LOGGER.info(f'Updated {len(posts)} lynx posts with images.')
    return make_response('Updated Lynx posts successfully.')
