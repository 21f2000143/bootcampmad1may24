from flask import current_app as app, render_template, request
from flask_login import login_required, current_user
from application.models import *
import random


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
