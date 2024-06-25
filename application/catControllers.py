from flask import current_app as app, request, flash, redirect, url_for, render_template
from flask_login import current_user, login_required, login_user
from application.models import *


@app.route('/add_category', methods=['POST'])
@login_required
def add_category():
    if current_user.is_admin:
        if request.method == 'POST':
            name = request.form['name']
            category=None
            category = Category.query.filter_by(name=name).first()
            if category:
                flash("This category already exits. Category should be unique!")
                return redirect(url_for('dashboard_admin'))
            else:
                category = Category(name=name, view_type='category')
                db.session.add(category)
                db.session.commit()
                flash("Category created in the database.")
                return redirect(url_for('dashboard_admin'))
    else:
        return "No permission"

@app.route('/add_category/update/<int:id>', methods=['POST'])
@login_required
def add_category_update(id):
    if current_user.is_admin:
        if request.method == 'POST':
            name = request.form['name']
            category=None
            category = Category.query.filter_by(id=id).first()
            if category:
                category.name=name
                db.session.commit()
                flash(f'The category update to {name}!')
                return redirect(url_for('dashboard_admin'))
            else:
                flash("Something went wrong while updating the category.")
                return redirect(url_for('dashboard_admin'))
    else:
        return "No permission"
        
@app.route('/add_category/delete/<int:id>')
@login_required
def add_category_delete(id):
    if current_user.is_admin:
        category=None
        category = Category.query.filter_by(id=id).first()
        name = category.name
        if category:
            for product in category.products:
                db.session.delete(product)
                db.session.commit()
            db.session.delete(category)
            db.session.commit()
            flash(f'{name} category deleted')
            return redirect(url_for('dashboard_admin'))
        else:
            flash("Something went wrong while deleting the category.")
            return redirect(url_for('dashboard_admin'))
    else:
        return "No permission"