UPDATE
	posts
SET
	plaintext = REPLACE(plaintext, 'http://', 'https://')
WHERE
	plaintext LIKE '%%http://%%';