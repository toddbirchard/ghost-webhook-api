UPDATE
	tags
SET og_image = feature_image
WHERE
	feature_image IS NOT NULL
	AND og_image != feature_image;