UPDATE
	posts
SET
	status = 'draft'
WHERE
	custom_excerpt IS NULL
	AND TYPE = 'post'
	AND status = 'published';