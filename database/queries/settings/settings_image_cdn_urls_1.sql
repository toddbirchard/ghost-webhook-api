UPDATE
    settings
SET
    value = REPLACE(value, 'https://storage.googleapis.com/hackersandslackers-cdn/', 'https://cdn.hackersandslackers.com/')
WHERE
      value LIKE '%%https://storage.googleapis.com/hackersandslackers-cdn/%%';