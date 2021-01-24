UPDATE
	posts
SET
	plaintext = REPLACE(plaintext, 'http://', 'https://')
WHERE
	title LIKE '%%Lynx%%'
    AND plaintext LIKE '%%http://%%';