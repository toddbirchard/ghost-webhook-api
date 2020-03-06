UPDATE
	posts
SET
	custom_excerpt = REPLACE(custom_excerpt, '\"', '\'')
WHERE
	custom_excerpt LIKE '%%\"%%';
