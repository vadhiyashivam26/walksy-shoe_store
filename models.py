import datetime
from flask import Flask 
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from sqlalchemy import true
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:2636@localhost/walksy'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# db = SQLAlchemy(app)
db = SQLAlchemy()
db.init_app()

class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)  # Store hashed passwords
    is_admin = db.Column(db.Boolean, default=False)  # True for admin, False for normal user

    def __repr__(self):
        return f"<User {self.email}>"

class Product(db.Model):
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    brand = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    size = db.Column(db.Integer)
    color = db.Column(db.String(50))
    image_url = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return f"<Product {self.name}>"

class Order(db.Model):
    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    total_amount = db.Column(db.Numeric(10, 2), nullable=False)
    status = db.Column(db.String(50), default='Placed')
    address = db.Column(db.Text, nullable=False)
    payment_method = db.Column(db.String(50), nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = db.relationship('User', backref='orders')    
    product = db.relationship('Product', backref='orders')

class CartItem(db.Model):
    __tablename__ = 'cart_items'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=1)
    added_at = db.Column(db.DateTime, server_default=db.func.now())

    user = db.relationship('User', backref='cart_items')
    product = db.relationship('Product', backref='cart_items')

class Contact(db.Model):
    __tablename__ = 'Contact'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    message = db.Column(db.Text, nullable=False)
    submitted_at = db.Column(db.DateTime, default=datetime.utcnow)

# with app.app_context():
#     db.drop_all()
#     db.create_all()