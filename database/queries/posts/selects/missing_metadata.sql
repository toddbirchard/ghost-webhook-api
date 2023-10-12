SELECT 
	posts.id, 
	posts.slug,
    posts.title,
    posts_meta.meta_title,
    posts_meta.meta_description,
    posts_meta.feature_image_alt,
    posts_meta.feature_image_caption,
    posts_meta.og_image,
    posts_meta.og_description,
    posts_meta.og_description,
    posts_meta.twitter_title,
    posts_meta.twitter_description,
    posts_meta.twitter_image
FROM posts
LEFT JOIN posts_meta ON posts.id = posts_meta.post_id;