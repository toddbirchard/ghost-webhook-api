UPDATE
	posts
SET
	html = REPLACE(html, 'http://', 'https://')
WHERE
	title LIKE '%%Lynx%%'
	AND html LIKE '%http://%%';