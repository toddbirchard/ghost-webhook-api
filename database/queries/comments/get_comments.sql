SELECT
	id,
	post_id,
	member_id,
	parent_id,
	html,
	edited_at,
	created_at
FROM
	comments
WHERE
	status = 'published'
ORDER BY
	edited_at DESC;