UPDATE
	posts
SET
	mobiledoc = REPLACE(mobiledoc, 'http://', 'https://')
WHERE
	mobiledoc LIKE '%%http://%%';