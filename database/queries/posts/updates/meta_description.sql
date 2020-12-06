UPDATE
    posts,
	posts_meta
SET
	posts_meta.meta_description = posts.custom_excerpt
WHERE
	posts_meta.meta_description IS NULL
	AND posts.custom_excerpt IS NOT NULL
	AND posts.id = posts_meta.post_id;
