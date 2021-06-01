UPDATE
	posts
SET
	status = 'draft'
WHERE
	feature_image IS NULL
	AND TYPE = 'post'
	AND status = 'published';