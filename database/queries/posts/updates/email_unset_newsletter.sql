UPDATE
	posts
SET
	email_recipient_filter = 'none'
WHERE
	email_recipient_filter != 'none'
	AND created_by != 1;