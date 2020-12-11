UPDATE
    posts,
	posts_meta
SET
	posts_meta.meta_title = posts.title
WHERE
	posts_meta.meta_title IS NULL
	AND posts.title IS NOT NULL
	AND posts.id = posts_meta.post_id;
