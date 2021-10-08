UPDATE
    settings
SET
    value = REPLACE(value, 'https://hackersandslackers-cdn.storage.googleapis.com/', 'https://cdn.hackersandslackers.com/')
WHERE
      value LIKE '%https://hackersandslackers-cdn.storage.googleapis.com/%';