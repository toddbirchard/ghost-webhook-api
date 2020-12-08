SELECT
  REPLACE(title, ' - Hackers and Slackers', '') as title,
  url,
  REPLACE(REPLACE(url, 'https://hackersandslackers.com/', ''), '/' , '') as slug,
  COUNT(title) AS views
FROM
  hackersgatsbyprod.pages
WHERE
  timestamp >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 7 day)
  AND url NOT LIKE '%/page/%'
  AND url NOT LIKE '%/tag/%'
  AND url NOT LIKE '%/series/%'
  AND url NOT LIKE '%/author/%'
  AND title IS NOT NULL
GROUP BY
  url,
  title
ORDER BY
  COUNT(url) DESC
LIMIT
  100;
