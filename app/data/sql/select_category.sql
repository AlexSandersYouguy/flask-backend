SELECT DISTINCT name 
FROM categories 
WHERE name IS NOT NULL AND name != ''
ORDER BY name ASC;