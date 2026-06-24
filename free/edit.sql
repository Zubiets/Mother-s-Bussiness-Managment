SELECT categories.*, suppliers.name
FROM categories
JOIN suppliers ON categories.suppliers_id = suppliers.id
WHERE categories.name = 'mundial';