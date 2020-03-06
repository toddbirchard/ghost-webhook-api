UPDATE
    posts,
	posts_meta
SET
	posts_meta.twitter_description = posts.custom_excerpt
WHERE
	posts_meta.twitter_description IS NULL
	AND posts.custom_excerpt IS NOT NULL;
