UPDATE
	posts
SET
	plaintext = REPLACE(plaintext, 'https://hackersandslackers-cdn.storage.googleapis.com', 'https://cdn.hackersandslackers.com')
WHERE
	plaintext LIKE '%https://hackersandslackers-cdn.storage.googleapis.com%';