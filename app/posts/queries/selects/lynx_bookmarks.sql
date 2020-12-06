SELECT
    id,
    slug,
	title,
	html,
	mobiledoc
FROM
	posts
WHERE
	title LIKE '%%Lynx%%'
	AND status IN ('scheduled', 'draft')
	AND mobiledoc NOT LIKE '%%bookmark%%'
    LIMIT 1;