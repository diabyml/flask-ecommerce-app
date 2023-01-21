import os
from flask import Flask,render_template,request,redirect,url_for,session,jsonify,make_response
from werkzeug.utils import secure_filename
from flask_session import Session
from tempfile import mkdtemp
from cs50 import SQL

from helpers import errored,allowed_file,make_unique,admin_required,validate_inputs
from sql_utils import is_admin,get_categories,add_product,get_all_products,get_product,delete_product,\
    get_unique_filename,update_product,update_product_filenames,get_products_for_home,\
        get_products,get_product_detail

UPLOAD_FOLDER = 'static/uploads/'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

db = SQL("sqlite:///dambeshop.db")

# configure session
# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.route("/")
def index():
    data = get_products_for_home(db)
    categories_data = get_categories(db)
    categories = {}
    for category in categories_data:
        categories[category['title'].lower()] = category['title']
    return render_template('index.html',data=data,categories=categories)

@app.route('/products/<category_title>')
def category(category_title):
    products = get_products(db,category_title,-1)
    # print(products)
    return render_template('category-list.html',category_title=category_title,products=products)



@app.route('/product/<product_id>')
def product(product_id):
    product = get_product_detail(db,product_id)
    print(product)
    return render_template('product.html',product=product)


@app.route('/display/<filename>')
def display_image(filename):
	print('display_image filename: ' + filename)
	return redirect(url_for('static', filename='uploads/' + filename), code=301)


# admin routes 
# addmin route
@app.route('/admin',methods=['POST','GET'])
def admin():
    if request.method == 'POST':
        username = request.form.get('username')
        pwd = request.form.get('password')

        if not username or not pwd:
            return render_template('apology.html',message='Username aand/or password empty'),403
        
        # check admin information
        if is_admin(db,username,pwd):
            session['admin'] = username
            return redirect("/admin/dashboard")
        else:
            errored(message='Wrong username and/ or password',code=401)

    # check if admin is logged in and redirect him to dashboard
    if session.get('admin'):
        return redirect("/admin/dashboard")

    return render_template('/admin/admin.html')

@app.route('/admin/dashboard')
@admin_required
def admin_dashboard():
    products = get_all_products(db)
    # print(products)
    return render_template('/admin/dashboard.html',products=products)

@app.route("/admin/dashboard/<product_id>")
def edit_product(product_id):
    categories = get_categories(db)
    product = get_product(db,product_id)
    # print("Product category:",product)
    return render_template('/admin/edit_product.html',categories=categories,product=product)

@app.route('/admin/add',methods=['POST','GET'])
@admin_required
def add():
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        price = request.form.get('price')
        photo = request.files.get('photo')
        category = request.form.get('category')
        
        if not name:
            return errored("Le nonm ne peut pas etre vide",code=401)
        if not description:
            return errored("La description  ne peut pas etre vide",code=401)
        if not price:
            return errored("Le prix ne peut pas etre vide",code=401)
        if not photo:
            return errored("La photo ne peut pas etre vide",code=401)
        if not category:
            return errored("La category ne peut pas etre vide",code=401)
        
        if allowed_file(photo.filename,ALLOWED_EXTENSIONS):
            filename = secure_filename(photo.filename)
            unique_filename = make_unique(filename)
            photo.save(os.path.join(app.config['UPLOAD_FOLDER'], unique_filename))
            # whene uplaoding to db
            # we upload the original filename, and uinque filenAME

            # convert price to int
            price = int(price)
            product = {
                'name':name,
                'description':description,
                'price':price,
                'original_filename':filename,
                'unique_filename': unique_filename,
                'category_id': category,
                'admin_username': session['admin']
            }
            # print(product)
            print('adding....')
            add_product(db, product)
            return redirect('/admin/dashboard')
        else:
            # the format of the photo is not accepted
            return errored("Le format de cette photo n'est pa accepte !",code=401)

    # GET REQUEST  
    categories = get_categories(db)
    return render_template("/admin/add.html",categories=categories)

#update a product 
@app.route("/admin/dashboard/update",methods=["POST"])
def update():
    if request.method == "POST":
        product_id = request.form.get("id")
        name = request.form.get('name')
        description = request.form.get('description')
        price = request.form.get('price')
        photo = request.files.get('photo')
        category = request.form.get('category')
        
        if not name:
            return errored("Le nom ne peut pas etre vide",code=401)
        if not description:
            return errored("La description  ne peut pas etre vide",code=401)
        if not price:
            return errored("Le prix ne peut pas etre vide",code=401)
        if not category:
            return errored("La category ne peut pas etre vide",code=401)

        
        # save product info
        price = int(price)
        update_product(db,{
            'id':product_id,
            'name':name,
            'description':description,
            'price':price,
            'category_id':category
        })

        if photo:
            # user picks a photo

            # delete existing photo
            filename = get_unique_filename(db,product_id)
            if os.path.join(app.config['UPLOAD_FOLDER'],filename):
                os.remove(os.path.join(app.config['UPLOAD_FOLDER'],filename))

            # add new photo
            if allowed_file(photo.filename,ALLOWED_EXTENSIONS):
                filename = secure_filename(photo.filename)
                unique_filename = make_unique(filename)
                photo.save(os.path.join(app.config['UPLOAD_FOLDER'], unique_filename))
                update_product_filenames(db,{
                    'id':product_id,
                    'original_filename':filename,
                    'unique_filename':unique_filename
                })
            
            


        return redirect('/admin/dashboard')
            

# delete product functionnality
@app.route("/admin/dashboard/delete",methods=['POST'])
def dashboard_delete_product():
    if request.method == 'POST':
        product_id = request.get_json()['product_id']

        # delete image from the server
        filename = get_unique_filename(db,product_id)
        if os.path.join(app.config['UPLOAD_FOLDER'],filename):
            os.remove(os.path.join(app.config['UPLOAD_FOLDER'],filename))
        else:
            return errored("Une erreur s'est produite lors de la suppression de la photo, veillez reessayez")

        result = delete_product(db,product_id)
        result = ''
        if result:
            # delete success and return 200
            return make_response(jsonify({'status':'ok'},200))
        else:
            # delete is not success 500
            return make_response(jsonify({'status':'no'},500))