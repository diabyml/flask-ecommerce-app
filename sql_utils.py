from werkzeug.security import check_password_hash

def is_admin(db,username,pwd):
        admin_query = db.execute("SELECT * FROM admins WHERE username=? LIMIT 1",username)
        if admin_query:
            admin = admin_query[0]
            if check_password_hash(admin['hash'],pwd):
                # return render_template('admin/dashboard.html')
                return True
            else:
                # return errored(message='Wrong password',code=401)
                return False

def get_categories(db):
    return db.execute("SELECT * FROM categories")

def get_category_id(db,title):
    category_id = db.execute('SELECT id FROM categories WHERE title=?',title)
    return category_id

def get_category_title(db,category_id):
    return db.execute('SELECT title FROM categories WHERE id=?',category_id)[0]['title']

def get_product(db,product_id):
    return db.execute('''SELECT products.id,products.name,description,price,categories.title as category 
                        FROM products,categories 
                        WHERE categories.id = category_id 
                        AND products.id=?''',product_id)[0]

def get_unique_filename(db,product_id):
    return db.execute("SELECT unique_filename FROM products WHERE id=?",product_id)[0]['unique_filename']

def add_product(db,product):
    db.execute('''INSERT INTO products (name,description,price,
                original_filename,unique_filename,category_id,
                admin_username) VALUES (?,?,?,?,?,?,?)''',
                product['name'],product['description'],
                product['price'],product['original_filename'],
                product['unique_filename'],product['category_id'],
                product['admin_username'])


# get all products by order
def get_all_products(db,order="DESC"):
    # order possible values: DESC - asc
    return db.execute('''SELECT products.id,products.name,price,timestamp,unique_filename,description,
    categories.title as category,admins.username as admin_username,
    admins.phone as admin_phone
    FROM products,categories,admins 
    WHERE products.category_id = categories.id
    AND products.admin_username = admins.username ORDER BY timestamp DESC''')

def get_products(db,category_title,numElements):
    if numElements > 0:
        return  db.execute('''SELECT products.id as id,name,price,unique_filename,description
                    FROM products,categories
                    WHERE products.category_id = categories.id
                    AND categories.title =?
                    ORDER BY timestamp DESC LIMIT ?''',category_title,numElements)
    
    return  db.execute('''SELECT products.id as id,name,price,unique_filename,description 
                    FROM products,categories
                    WHERE products.category_id = categories.id
                    AND categories.title =?
                    ORDER BY timestamp DESC''',category_title)

def get_products_for_home(db):
    products = {}

    # hommes = db.execute('''SELECT products.id as id,name,price,unique_filename FROM products,categories
    #              WHERE products.category_id = categories.id
    #              AND categories.title =?
    #              ORDER BY timestamp DESC LIMIT 4''','Hommes')
    

    
    products['hommes'] = get_products(db,'Hommes',4)
    products['femmes'] = get_products(db,'Femmes',4)
    products['arts'] = get_products(db,'Arts',4)
    products['divers'] = get_products(db,'Divers',4)
    return products

def get_product_detail(db,product_id):
    return db.execute('''SELECT products.name,price,description,timestamp,unique_filename,
                title as category, username as admin_username, phone as admin_phone,whatsapp admin_whatsapp
                FROM products,categories,admins 
                WHERE products.admin_username = admins.username
                AND products.category_id = categories.id 
                AND products.id =?''',product_id)[0]

def delete_product(db,product_id):
    try:
        db.execute("DELETE FROM products WHERE id=?",product_id)
        return True
    except BaseException as e:
        return False

def update_product(db,product):
    db.execute('''UPDATE products SET name=?,description=?,price=?,category_id=?
                    WHERE id=?''', 
                     product['name'],
                     product['description'],
                     product['price'],
                     product['category_id'],
                     product['id'])

def update_product_filenames(db,product):
    db.execute('''UPDATE products SET original_filename=?, unique_filename=?
                WHERE id=?''',
                product['original_filename'],
                product['unique_filename'],
                product['id'])
