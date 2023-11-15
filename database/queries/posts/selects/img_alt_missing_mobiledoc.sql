SELECT
	id,
    mobiledoc
FROM
	posts
WHERE
	mobiledoc LIKE '%["image"%'
	AND mobiledoc NOT LIKE '%"alt":"%'
	AND status = 'published';