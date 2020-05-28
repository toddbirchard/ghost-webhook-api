UPDATE
	posts
SET
	plaintext = REPLACE(plaintext, 'http://', 'https://')
WHERE
	status IN('scheduled', 'draft')
	AND title LIKE '%Lynx%'