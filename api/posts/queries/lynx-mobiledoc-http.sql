UPDATE
	posts
SET
	mobiledoc = REPLACE(mobiledoc, 'http://', 'https://')
WHERE
	status IN('scheduled', 'draft')
	AND title LIKE '%Lynx%'