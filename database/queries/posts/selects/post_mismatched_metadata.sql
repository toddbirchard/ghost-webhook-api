SELECT
	posts.id,
	posts.slug,
	posts.title,
	posts.custom_excerpt,
	posts.feature_image,
	posts_meta.meta_title,
	posts_meta.meta_description,
	posts_meta.og_title,
	posts_meta.og_image,
	posts_meta.og_description,
	posts_meta.twitter_title,
	posts_meta.twitter_description,
	posts_meta.twitter_image
FROM
	posts
	LEFT JOIN posts_meta ON posts.id = posts_meta.post_id
WHERE
	posts.type = 'post'
	AND (posts.title != posts_meta.og_title
		OR posts.custom_excerpt != posts_meta.og_description
		OR posts.custom_excerpt != posts_meta.twitter_description
		OR posts.feature_image IS NOT NULL
		OR (posts_meta.og_image IS NULL OR posts_meta.twitter_image IS NULL));