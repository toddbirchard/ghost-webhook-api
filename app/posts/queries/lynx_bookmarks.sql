SELECT
    id,
	title,
	html
FROM
	posts
WHERE
	title LIKE '%%Lynx%%'
	AND status = 'scheduled'
	AND html NOT LIKE '%%kg-bookmark-card%%';