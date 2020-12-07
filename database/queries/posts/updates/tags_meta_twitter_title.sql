UPDATE
	tags
SET twitter_title = meta_title
WHERE
	meta_title IS NOT NULL
	AND twitter_title IS NULL;