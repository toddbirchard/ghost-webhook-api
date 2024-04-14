UPDATE
	users
SET
	cover_image = REPLACE(cover_image, 'https://hackersandslackers-cdn.storage.googleapis.com/', 'https://cdn.hackersandslackers.com/')
WHERE
	cover_image LIKE 'https://hackersandslackers-cdn.storage.googleapis.com/%%';