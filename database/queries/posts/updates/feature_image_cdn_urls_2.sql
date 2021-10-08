UPDATE
	posts
SET
	feature_image = REPLACE(feature_image, 'https://storage.googleapis.com/hackersandslackers-cdn/', 'https://cdn.hackersandslackers.com/')
WHERE
	feature_image LIKE '%https://storage.googleapis.com/hackersandslackers-cdn/%';