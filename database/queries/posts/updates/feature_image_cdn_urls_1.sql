UPDATE
	posts
SET
	feature_image = REPLACE(feature_image, 'https://hackersandslackers-cdn.storage.googleapis.com/', 'https://cdn.hackersandslackers.com/')
WHERE
	feature_image LIKE '%%https://hackersandslackers-cdn.storage.googleapis.com/%%';