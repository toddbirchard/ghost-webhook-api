UPDATE
	users
SET
	profile_image = REPLACE(profile_image, 'https://hackersandslackers-cdn.storage.googleapis.com/', 'https://cdn.hackersandslackers.com/')
WHERE
	profile_image LIKE 'https://hackersandslackers-cdn.storage.googleapis.com/%%';