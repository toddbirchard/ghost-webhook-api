UPDATE
	tags
SET twitter_image = feature_image
WHERE
	feature_image IS NOT NULL
	AND twitter_image != feature_image;