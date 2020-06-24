SELECT
    id,
	feature_image,
	title
FROM
	posts
WHERE
	feature_image = ''
	AND title LIKE '%%Lynx%%';