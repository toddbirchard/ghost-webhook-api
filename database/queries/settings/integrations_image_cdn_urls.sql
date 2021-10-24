UPDATE
	integrations
SET
	icon_image = REPLACE(icon_image, 'https://hackersandslackers-cdn.storage.googleapis.com/', 'https://cdn.hackersandslackers.com/')
WHERE
	icon_image LIKE '%%https://hackersandslackers-cdn.storage.googleapis.com/%%';