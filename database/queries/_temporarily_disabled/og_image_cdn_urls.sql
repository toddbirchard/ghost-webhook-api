UPDATE
	posts_meta
SET
	og_image = REPLACE(og_image, 'https://storage.googleapis.com/hackersandslackers-cdn/', 'https://cdn.hackersandslackers.com/')
WHERE
	og_image LIKE '%https://storage.googleapis.com/hackersandslackers-cdn/%';