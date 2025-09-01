from operator import or_
from tempfile import template
from flask import Flask, render_template, redirect, template_rendered, url_for, flash , request 
from models import Contact, User, Product, Order, CartItem , db
import os
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
from flask_login import LoginManager, current_user, login_required, login_user, logout_user
from flask_bcrypt import Bcrypt
from functools import wraps
from dotenv import load_dotenv


# Load .env variables
load_dotenv()

app = Flask(__name__)

# for hashed password
bcrypt = Bcrypt(app)

# for login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = "Please log in to access this page."
login_manager.login_message_category = "danger"

#upload files on static folder and store image path into db
UPLOAD_FOLDER = 'static/images/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)


# app.secret_key = 'supersecretkey'
app.secret_key = os.getenv("DB_URL")

# Database connection string
# db_user = os.getenv("DB_USER")
# db_pass = os.getenv("DB_PASS")
# db_host = os.getenv("DB_HOST")
# db_name = os.getenv("DB_NAME")

# connect MYSQL with sqlAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = app.secret_key
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    "connect_args": {
        "ssl": {}  # empty dict enables SSL without certificates
    }
}
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:2636@localhost/walksy'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            flash("Oops, you'r not an Admin !", "danger")
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

#client routes
@app.route('/')
@app.route('/home')
def home():
    product = Product.query.filter_by(description='Featured product').all()
    return render_template("index.html", products=product)

@app.route('/home/about')
def about():
    return render_template('about.html')

@app.route("/home/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        subject = request.form.get("subject")
        message = request.form.get("message")

        # Save to DB
        new_message = Contact(
            name=name,
            email=email,
            message=message
        )
        db.session.add(new_message)
        db.session.commit()

        flash("Thank you for reaching out!", "success")
        return redirect("/home/contact")

    return render_template("contact.html")

@app.route('/home/men')
def men():
    brand = request.args.get('brand')
    gender = request.args.get('category', 'male')  # default to 'female'

    # Base query for female category
    base_query = Product.query.filter(Product.category == gender)

    # If brand filter is applied
    if brand:
        base_query = base_query.filter(Product.brand == brand)

    products = base_query.all()

    return render_template("men.html", products=products, selected_brand=brand, selected_gender=gender)

@app.route('/home/women')
def women():
    brand = request.args.get('brand')
    gender = request.args.get('category', 'female')  # default to 'female'

    # Base query for female category
    base_query = Product.query.filter(Product.category == gender)

    # If brand filter is applied
    if brand:
        base_query = base_query.filter(Product.brand == brand)

    products = base_query.all()

    return render_template("women.html", products=products, selected_brand=brand, selected_gender=gender)

@app.route('/home/category')
def category():
    brand = request.args.get('brand')
    gender = request.args.get('category')

    # Base query for male and female categories
    base_query = Product.query.filter(or_(
        Product.category == 'male',
        Product.category == 'female'
    ))

    # If brand is provided in the query parameter, apply filter
    if brand:
        base_query = base_query.filter_by(brand=brand)
    if gender:
        base_query = base_query.filter_by(category=gender)    

    products = base_query.all()

    return render_template("category.html", products=products, selected_brand=brand)

@app.route('/home/product/<int:product_id>')
def shoe_details(product_id):
    product = Product.query.get_or_404(product_id)
    return render_template('shoe_details.html', product=product)

@app.route('/home/cart')
@login_required
def cart():
    cart_items = CartItem.query.filter_by(user_id=current_user.id).all()
    total_price = sum(item.quantity * item.product.price for item in cart_items)

    return render_template('cart.html', cart_items=cart_items, total=total_price)

@app.route('/home/add_to_cart/<int:product_id>')
@login_required
def add_to_cart(product_id):
    product = Product.query.get_or_404(product_id)
    item = CartItem(user_id=current_user.id, product_id=product.id)
    db.session.add(item)
    db.session.commit()
    flash('Product added to cart!', 'success')
    return redirect(url_for('cart', product_id=product.id))

@app.route('/home/cart/update_cart', methods=['POST'])
@login_required
def update_cart():
    for key in request.form:
        if key.startswith('qty_'):
            cart_item_id = int(key.split('_')[1])
            new_qty = int(request.form[key])

            item = CartItem.query.get(cart_item_id)
            if item and item.user_id == current_user.id:
                if new_qty > 0:
                    item.quantity = new_qty
                else:
                    db.session.delete(item)

    db.session.commit()
    flash("Cart update successfully!.", "success")
    return redirect(url_for('cart'))

@app.route('/home/cart/remove_from_cart/<int:cart_item_id>')
@login_required
def remove_from_cart(cart_item_id):
    item = CartItem.query.get(cart_item_id)
    if item and item.user_id == current_user.id:
        db.session.delete(item)
        db.session.commit()
        flash("Item removed successfully!.", "danger")
    return redirect(url_for('cart'))

@app.route('/home/buy_now/<int:product_id>', methods=['POST'])
@login_required
def buy_now(product_id):
    product = Product.query.get_or_404(product_id)
    
    order = Order(product_id=product.id, user_id=current_user.id)
    db.session.add(order)
    db.session.commit()
    
    flash("Order was placed successfully!", "success")
    return redirect(url_for('product_details', product_id=product.id))

@app.route('/home/orders')
@login_required
def orders():
    user_orders = Order.query.filter_by(user_id=current_user.id).order_by(Order.id.desc()).all()
    return render_template('orders.html', orders=user_orders)

@app.route('/home/order/<int:product_id>', methods=['POST'])
@login_required
def place_order(product_id):
    product = Product.query.get_or_404(product_id)

    address = request.form.get('address')
    payment_method = request.form.get('payment_method')

    if not address or not payment_method:
        flash("Please provide all required fields.", "danger")
        return redirect(url_for('product_details', product_id=product_id))

    order = Order(
        user_id=current_user.id,
        product_id=product.id,
        total_amount=product.price,
        status='Placed',
        address=address,
        payment_method=payment_method
    )
    db.session.add(order)
    db.session.commit()

    flash("Order placed successfully!", "success")
    return redirect(url_for('orders'))

# admin main page routes
@app.route('/admin')
@admin_required
def admin_dashboard():
    product = Product.query.all()
    return render_template('admin/dashboard.html', products=product )

@app.route('/admin/add', methods=['GET', 'POST'])
@admin_required
def add_shoe():
    if request.method == 'POST':
        name = request.form['name']
        price = request.form['price']
        description = request.form['description']
        brand = request.form['brand']
        category = request.form['category']
        size = request.form['size']
        color = request.form['color']
        image_file = request.files.get('image_file')

        image_url = ''
        if image_file and image_file.filename != '':
            filename = secure_filename(image_file.filename)
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            image_file.save(image_path)
            image_url = f'images/uploads/{filename}'  

        # Save product with image_url
        new_product = Product(
            name=name,
            price=price,
            description=description,
            brand=brand,
            category=category,
            size=size,
            color=color,
            image_url=image_url 
        )
        print('image_url:', image_url)
        db.session.add(new_product)
        db.session.commit()
        flash("Shoe added successfully!", "success")
        return redirect(url_for('admin_dashboard'))

    return render_template('admin/add_shoe.html')

#admin edit route
@app.route('/admin/edit/<int:id>', methods=['GET', 'POST'])
@admin_required
def edit_shoe(id):
    shoe = Product.query.get_or_404(id)

    if request.method == 'POST':
        shoe.name = request.form['name']
        shoe.description = request.form['description']
        shoe.price = request.form['price']
        shoe.brand = request.form['brand']
        shoe.category = request.form['category']
        shoe.size = request.form['size']
        shoe.color = request.form['color']
        
        db.session.commit()
        flash("Shoe updated successfully!", "success")
        return redirect(url_for('admin_dashboard'))
    
    return render_template('admin/edit_shoe.html', shoe=shoe)

#product delete route
@app.route('/admin/delete/<int:id>', methods=['GET'])
@admin_required
def delete_shoe(id):
    product = Product.query.get_or_404(id)
    db.session.delete(product)
    db.session.commit()
    flash("Product deleted Successfully!", "danger")
    return redirect('/admin')

# Admin - View all users
@app.route('/admin/users')
@login_required
@admin_required
def admin_users():
    if not current_user.is_admin:
        return redirect(url_for('home'))
    users = User.query.all()
    return render_template('admin/admin_users.html', users=users)

# Admin - View all orders
@app.route('/admin/orders')
@login_required
@admin_required
def admin_orders():
    if not current_user.is_admin:
        return redirect(url_for('home'))
    orders = Order.query.all()
    return render_template('admin/admin_orders.html', orders=orders)

@app.route('/admin/contact')
@login_required
@admin_required
def view_contact_messages():
    if not current_user.is_admin:
        return redirect(url_for('home'))

    messages = Contact.query.order_by(Contact.submitted_at.desc()).all()
    return render_template('admin/contact.html', messages=messages)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = bcrypt.generate_password_hash(request.form['password']).decode('utf-8')

        new_user = User(name=name, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()
        flash("Registration successful. Please login.", "success")
        return redirect(url_for('login'))
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        name = request.form['name']
        password = request.form['password']

        user = User.query.filter_by(name=name).first()
        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            flash("Welcome Back to Walksy!", "success")
            return redirect(url_for('home'))
        else:
            flash("Enter valid password", "danger")
    return render_template("login.html")

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You'r logged out now", "danger")
    return redirect('/home')

@app.route('/home/members', methods=['GET', 'POST'])
@login_required
def members():
    if request.method == 'POST' :
        return redirect("/home/category")
    
    flash("Connect with the Walksy. Become One of Us!", "info")
    return render_template("members.html")


if __name__ == '__main__':
    print('DB connected ')
    app.run(debug=True)
