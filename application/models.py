from application.database import db
from flask_login import UserMixin
from werkzeug.security import check_password_hash



class Product(db.Model): 
    id = db.Column(db.Integer, primary_key=True, autoincrement=True) 
    name = db.Column(db.String(100), nullable=False)
    img_name = db.Column(db.String(100), nullable=False)
    mgf_date = db.Column(db.String(100), nullable=False)
    exp_date = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    view_type = db.Column(db.String(100), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
  
    def __init__(self, name, description, price, category_id, view_type, img_name, mgf_date, exp_date, quantity):
        self.name = name
        self.description = description
        self.price = price
        self.category_id = category_id
        self.view_type = view_type
        self.img_name = img_name
        self.mgf_date = mgf_date
        self.exp_date = exp_date
        self.quantity = quantity


class UserProduct(db.Model):
    __tablename__ = 'userproduct'
    id = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.Integer, nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    view_type = db.Column(db.String(100), nullable=False)
    products = db.relationship('Product', backref='category', lazy=True)

    def __init__(self, name, view_type):
        self.name = name
        self.view_type = view_type


class User(db.Model, UserMixin): # UserMixin provides methods such as is_active, is_authenticated, etc.
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    is_admin = db.Column(db.Boolean, nullable=False)
    total_value = db.Column(db.Float)
    orders = db.relationship('Order', backref='user', lazy=True)
    cart = db.relationship('Product', secondary='userproduct')

    def __init__(self, username, email, password, is_admin, total_value):
        self.username = username
        self.email = email
        self.password = password
        self.is_admin = is_admin
        self.total_value = total_value

    def verify_password(self, password):
        return check_password_hash(self.password, password)


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    img_name = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    order_date = db.Column(db.DateTime, nullable=False)
   
    def __init__(self, user_id, name, img_name, amount, order_date):
        self.user_id = user_id
        self.name = name
        self.img_name = img_name
        self.amount = amount
        self.order_date = order_date