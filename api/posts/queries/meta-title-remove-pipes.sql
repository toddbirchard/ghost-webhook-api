UPDATE
	posts_meta
SET
	meta_title = REPLACE(meta_title, ' | ', ' - ')
WHERE
	meta_title LIKE '%%|%%';
