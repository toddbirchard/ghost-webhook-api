UPDATE
	tags
SET og_image = feature_image
WHERE
	feature_image IS NOT NULL
	AND og_image IS NULL;

UPDATE
	tags
SET twitter_image = feature_image
WHERE
	feature_image IS NOT NULL
	AND twitter_image IS NULL;

UPDATE
	tags
SET og_title = meta_title
WHERE
	meta_title IS NOT NULL
	AND og_title IS NULL;

UPDATE
	tags
SET twitter_title = meta_title
WHERE
	meta_title IS NOT NULL
	AND twitter_title IS NULL;

UPDATE
	tags
SET og_description = meta_description
WHERE
	meta_description IS NOT NULL
	AND og_description IS NULL;

UPDATE
	tags
SET twitter_description = meta_description
WHERE
	meta_title IS NOT NULL
	AND twitter_description IS NULL;