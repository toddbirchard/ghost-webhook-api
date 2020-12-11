SELECT
	id,
       slug,
       title
FROM
	posts
WHERE
	id NOT IN(
		SELECT
			post_id FROM posts_meta)
			AND custom_excerpt IS NOT NULL;