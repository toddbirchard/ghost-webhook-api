UPDATE
	tags
SET
	meta_description = description
WHERE
	meta_description IS NULL
	AND description IS NOT NULL;
