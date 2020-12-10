SELECT
	id,
    mobiledoc
FROM
	posts
WHERE
	mobiledoc NOT LIKE '%%alt%%'
	AND mobiledoc LIKE '%%["image"%%'
	AND status = 'published';