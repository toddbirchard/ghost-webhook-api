from flask import current_app as api
from flask import jsonify, make_response
from api import gcs
from .fetch import fetch
from .transform import ImageTransformer


@api.route('/images')
def transform_images():
    """Transform image objects."""
    retina_imgs, standard_imgs = fetch(gcs, api.config['GCP_BUCKET_FOLDER'])
    transformer = ImageTransformer(gcs,
                                   api.config['GCP_BUCKET_NAME'],
                                   api.config['GCP_BUCKET_URL'],
                                   retina_imgs,
                                   standard_imgs)
    response = {
        'retina': len(transformer.retina_transform()),
        'standard': len(transformer.standard_transform())
    }
    return make_response(jsonify(response))
