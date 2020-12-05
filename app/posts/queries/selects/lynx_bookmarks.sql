SELECT
    id,
	title,
	html,
	mobiledoc
FROM
	posts
WHERE
	title LIKE '%%Lynx%%'
	AND status IN ('scheduled', 'draft')
	AND html NOT LIKE '%%kg-bookmark-card%%';