UPDATE
	tags
SET og_description = meta_description
WHERE
	meta_description IS NOT NULL
	AND og_description IS NULL;