"""Routes to transform post images."""
from flask import current_app as api
from flask import jsonify, make_response, request
from api import db, image
from api.log import LOGGER


@api.route('/images/transform', methods=['GET'])
def transform_recent_images():
    """Apply image transformations to images uploaded in the current month."""
    folder = request.args.get('directory', api.config['GCP_BUCKET_FOLDER'])
    retina_images = image.fetch_image_blobs(folder, 'retina')
    standard_images = image.fetch_image_blobs(folder, 'standard')
    LOGGER.info(f'Checking {len(retina_images)} retina and {len(standard_images)} standard images in {folder}')
    retina_result = image.bulk_transform_images(folder, standard_images, transformation='retina')
    standard_images = image.bulk_transform_images(folder, retina_images, transformation='standard')
    webp_images = image.bulk_transform_images(folder, retina_images, transformation='webp')
    response = {'retina': retina_result, 'standard': standard_images, 'webp': webp_images}
    LOGGER.info(f'Transformed images successfully: {response}')
    return make_response(jsonify(response))


@api.route('/images/transform/lynx', methods=['GET'])
def transform_lynx_images():
    """Apply image transformations to all `Lynx` images."""
    folder = 'roundup'
    lynx_images = image.fetch_image_blobs(folder)
    LOGGER.info(f'Checking {len(lynx_images)} images in {folder}')
    response = image.bulk_transform_images(folder, lynx_images, transformation='retina')
    LOGGER.info(f'Transformed {response} images successfully!')
    return make_response(jsonify({'SUCCESS': f'Transformed {response} images successfully!'}))


@api.route('/images/lynx', methods=['GET'])
def assign_missing_lynx_images():
    """Assign random image to Lynx posts which are missing a feature image."""
    results = db.execute_query_from_file('api/images/sql/lynx_missing_images.sql')
    posts = [result.id for result in results]
    for post in posts:
        new_feature_image = image.fetch_random_lynx_image()
        db.update_post_image(new_feature_image, post)
    LOGGER.info(f'Updated {len(posts)} lynx posts with images.')
    return make_response('Updated Lynx posts successfully.')
