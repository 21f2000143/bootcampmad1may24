from flask import current_app as app, request, flash, redirect, url_for, render_template
from flask_login import current_user, login_required, login_user, logout_user
from application.models import *
import random
from werkzeug.security import generate_password_hash


@app.route('/register', methods=['POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        is_admin = False  # Set this based on your registration logic

        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('Username already exists', 'danger')
            return redirect(url_for('register'))

        user = User(username=username, email=email,
                    password=generate_password_hash(password), is_admin=is_admin, total_value=0)
        db.session.add(user)
        db.session.commit()
        login_user(user)
        flash('Registration successful. Please log in.', 'success')
        return redirect(url_for('dashboard_user'))
    else:
        if current_user.is_authenticated:
            print(current_user.is_admin, type(current_user.is_admin), )
            if user.is_admin==1:
                flash('Admin Login successful', 'success')
                return redirect(url_for('dashboard_admin'))
            else:
                flash('User Login successful', 'success')
                return redirect(url_for('dashboard_user'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        remember = request.form.get('remember')
        if remember:
            remember=True
        else:
            remember=False
        user = User.query.filter_by(email=email).first()

        if user and user.verify_password(password):
            login_user(user, remember=remember)
            if user.is_admin==1:
                flash('Admin Login successful', 'success')
                return redirect(url_for('dashboard_admin'))
            else:
                flash('User Login successful', 'success')
                return redirect(url_for('dashboard_user'))
        else:
            flash('Invalid username or password', 'danger')
            return redirect(url_for('index'))
    else:
        if current_user.is_authenticated:
            if user.is_admin:
                flash('Admin Login successful', 'success')
                return redirect(url_for('dashboard_admin'))
            else:
                flash('User Login successful', 'success')
                return redirect(url_for('dashboard_user'))

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html', user=current_user)

@app.route('/dashboard/admin')
@login_required
def dashboard_admin():
    if current_user.is_admin==1:
        query_by_category = request.args.get('query_by_category') 
        query_by_word = request.args.get('query_by_word') 
        if query_by_category:
            category = Category.query.filter_by(id=int(query_by_category)).first()
            if category:
                categories = Category.query.all() 
                return render_template('manager.html', current_user=current_user, items=category.products, categories=categories, query_by_category=category.name)
        if query_by_word:
            items=[]
            items= Product.query.filter(Product.name.like('%'+query_by_word+'%')).all()
            if not items:
                items= Product.query.filter(Product.description.like('%'+query_by_word+'%')).all()
            if not items:
                items= Product.query.filter(Product.mgf_date.like('%'+query_by_word+'%')).all()
            if not items:
                items= Product.query.filter(Product.exp_date.like('%'+query_by_word+'%')).all()
            if not items:
                items= Product.query.filter(Product.price.like('%'+query_by_word+'%')).all()
            if not items:
                items= Category.query.filter(Category.name.like('%'+query_by_word+'%')).all() 
            categories = Category.query.all() 
            return render_template('manager.html', current_user=current_user, items=items, categories=categories, query_by_word=query_by_word)
        categories = Category.query.all() 
        products = Product.query.all()
        items = categories + products
        random.shuffle(items)
        return render_template('manager.html', current_user=current_user, items=items, categories=categories)
    else:
        return "No permission"

@app.route('/dashboard/user')
@login_required
def dashboard_user():
    if current_user.is_admin==0:
        query_by_category = request.args.get('query_by_category') 
        query_by_word = request.args.get('query_by_word') 
        if query_by_category:
            category = Category.query.filter_by(id=int(query_by_category)).first()
            if category:
                categories = Category.query.all()
                userproducts =UserProduct.query.filter_by(user_id=current_user.id).all()
                return render_template('user.html', current_user=current_user, items=category.products, categories=categories, query_by_category=category.name, userproducts=userproducts)
        if query_by_word:
            items=[]
            items= Product.query.filter(Product.name.like('%'+query_by_word+'%')).all()
            if not items:
                items= Product.query.filter(Product.description.like('%'+query_by_word+'%')).all()
            if not items:
                items= Product.query.filter(Product.mgf_date.like('%'+query_by_word+'%')).all()
            if not items:
                items= Product.query.filter(Product.exp_date.like('%'+query_by_word+'%')).all()
            if not items:
                items= Product.query.filter(Product.price.like('%'+query_by_word+'%')).all()
            if not items:
                items= Category.query.filter(Category.name.like('%'+query_by_word+'%')).all() 
            categories = Category.query.all()
            userproducts =UserProduct.query.filter_by(user_id=current_user.id).all()
            return render_template('user.html', current_user=current_user, items=items, categories=categories, query_by_word=query_by_word, userproducts=userproducts)
        categories = Category.query.all() 
        products = Product.query.all()
        items = categories + products
        random.shuffle(items)
        userproducts =UserProduct.query.filter_by(user_id=current_user.id).all()
        return render_template('user.html', current_user=current_user, items=items, categories=categories, userproducts=userproducts)
    else:
        return "No permission"

@app.route('/')
def index():
    if current_user.is_authenticated:
        if current_user.is_admin==0:
            return redirect(url_for('dashboard_user'))
        if current_user.is_admin==1:
            return redirect(url_for('dashboard_admin'))
    query_by_category = request.args.get('query_by_category') 
    query_by_word = request.args.get('query_by_word') 
    if query_by_category:
        category = Category.query.filter_by(id=int(query_by_category)).first()
        if category:
            categories = Category.query.all() 
            return render_template('index.html', items=category.products, categories=categories, query_by_category=category.name)
    if query_by_word:
        items=[]
        items= Product.query.filter(Product.name.like('%'+query_by_word+'%')).all()
        if not items:
            items= Product.query.filter(Product.description.like('%'+query_by_word+'%')).all()
        if not items:
            items= Product.query.filter(Product.mgf_date.like('%'+query_by_word+'%')).all()
        if not items:
            items= Product.query.filter(Product.exp_date.like('%'+query_by_word+'%')).all()
        if not items:
            items= Product.query.filter(Product.price.like('%'+query_by_word+'%')).all()
        if not items:
            items= Category.query.filter(Category.name.like('%'+query_by_word+'%')).all() 
        categories = Category.query.all() 
        return render_template('index.html', items=items, categories=categories, query_by_word=query_by_word)
    categories = Category.query.all() 
    products = Product.query.all()
    items = categories + products
    random.shuffle(items)
    return render_template('index.html', items=items, categories=categories)