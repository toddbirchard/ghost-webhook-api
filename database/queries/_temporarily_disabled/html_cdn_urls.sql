UPDATE
	posts
SET
	html = REPLACE(html, 'https://hackersandslackers-cdn.storage.googleapis.com', 'https://cdn.hackersandslackers.com')
WHERE
	html LIKE '%%https://hackersandslackers-cdn.storage.googleapis.com%%';