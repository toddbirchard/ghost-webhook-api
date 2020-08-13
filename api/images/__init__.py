"""Routes to transform post images."""
from flask import current_app as api
from flask import jsonify, make_response, request
from clients import db
from clients.log import LOGGER
from clients import gcs


@LOGGER.catch
@api.route('/image/transform', methods=['POST'])
def create_post_retina_image():
    """Create retina image on post update."""
    post = request.get_json()['post']['current']
    feature_image = post.get('feature_image')
    title = post.get('title')
    if feature_image is not None and '@2x' not in feature_image:
        LOGGER.info(f'Creating gcs. for updated post {title}.')
        new_image = gcs.create_single_retina_image(feature_image)
        return make_response(jsonify({title: new_image}))


@api.route('/images/transform', methods=['GET'])
def transform_recent_images():
    """Apply transformations to image uploaded within the current month."""
    folder = request.args.get('directory', api.config['GCP_BUCKET_FOLDER'])
    retina_images = gcs.fetch_image_blobs(folder, 'retina')
    standard_images = gcs.fetch_image_blobs(folder, 'standard')
    LOGGER.info(f'Checking {len(retina_images)} retina and {len(standard_images)} standard image in {folder}')
    retina, mobile = gcs.bulk_transform_images(folder, standard_images, retina_images)
    response = {'retina': retina, 'mobile': mobile}
    LOGGER.info(f'Transformed images successfully: {response}')
    return make_response(jsonify(response))


@api.route('/images/transform/lynx', methods=['GET'])
def transform_lynx_images():
    """Apply transformations to all `Lynx` images."""
    folder = 'roundup'
    lynx_images = gcs.fetch_image_blobs(folder)
    response = gcs.bulk_transform_images(folder, lynx_images, transformation='retina')
    LOGGER.info(f'Transformed {response} gcs. successfully!')
    return make_response(jsonify({'SUCCESS': f'Transformed {response} image successfully!'}))


@api.route('/images/assign/lynx', methods=['GET'])
def assign_missing_lynx_images():
    """Assign random image to Lynx posts which are missing a feature image."""
    results = db.execute_query_from_file(
        'api/images/sql/lynx_missing_images.sql',
        database_name='blog'
    )
    posts = [result.id for result in results]
    for post in posts:
        image = gcs.fetch_random_lynx_image()
        db.execute_query(
            f"UPDATE posts SET feature_image = '{image}' WHERE id = '{post}';",
            database_name='blog'
        )
    LOGGER.info(f'Updated {len(posts)} lynx posts with image.')
    return make_response(f'Updated {len(posts)} lynx posts with image.')
