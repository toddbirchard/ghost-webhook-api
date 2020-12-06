UPDATE
	posts
SET
	title = REPLACE(title, '\"', '\'')
WHERE
	title LIKE '%%\"%%';
