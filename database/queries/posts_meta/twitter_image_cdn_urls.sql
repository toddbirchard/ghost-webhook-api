UPDATE
    posts_meta
SET
    twitter_image = REPLACE(twitter_image, 'https://hackersandslackers-cdn.storage.googleapis.com', 'https://cdn.hackersandslackers.com')
WHERE
      twitter_image LIKE 'https://hackersandslackers-cdn.storage.googleapis.com%%';