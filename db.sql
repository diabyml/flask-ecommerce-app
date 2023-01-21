CREATE TABLE IF NOT EXISTS products(
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT NOT NULL,
    price INTEGER NOT NULL,
    original_filename TEXT NOT NULL,
    unique_filename TEXT NOT NULL,
    category_id INTEGER NOT NULL,
    admin_username TEXT NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (category_id) REFERENCES categories,
    FOREIGN KEY (admin_username) REFERENCES admins
);

CREATE TABLE IF NOT EXISTS admins(
    username TEXT NOT NULL PRIMARY KEY,
    hash TEXT NOT NULL,
    name TEXT NOT NULL,
    phone TEXT NOT NULL,
    whatsapp TEXT NOT NULL
);


-- get all products by order
SELECT products.id,products.name,price,timestamp,unique_filename,description,
    categories.title as category,admins.username as admin_username,
    admins.phone as admin_phone
    FROM products,categories,admins 
    WHERE products.category_id = categories.id
    AND products.admin_username = admins.username ORDER BY timestamp DESC;