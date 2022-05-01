UPDATE
	tags
SET
	og_image = REPLACE(og_image, 'https://hackersandslackers-cdn.storage.googleapis.com/', 'https://cdn.hackersandslackers.com/')
WHERE
	og_image LIKE 'https://hackersandslackers-cdn.storage.googleapis.com/%%';