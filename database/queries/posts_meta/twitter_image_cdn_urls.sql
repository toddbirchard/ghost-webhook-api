UPDATE
	posts_meta
SET
	twitter_image = REPLACE(twitter_image, 'https://storage.googleapis.com/hackersandslackers-cdn/', 'https://cdn.hackersandslackers.com/')
WHERE
	twitter_image LIKE '%%https://storage.googleapis.com/hackersandslackers-cdn/%%';