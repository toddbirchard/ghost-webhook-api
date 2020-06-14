"""Post feature image transformations."""
from api.log import LOGGER
from api import image


def optimize_feature_image(feature_image):
	"""Create retina version of feature image."""
	new_feature_image = image.transform_single_image(feature_image)
	LOGGER.info(f'Generated retina image {new_feature_image}.')
	return new_feature_image
