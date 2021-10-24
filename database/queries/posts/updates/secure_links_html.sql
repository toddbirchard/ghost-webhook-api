UPDATE
	posts
SET
	html = REPLACE(html, 'http://', 'https://')
WHERE
	html LIKE '%%http://%%';