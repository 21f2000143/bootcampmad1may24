from flask import current_app as app, request, flash, redirect, url_for, render_template
from flask_login import current_user, login_required, login_user
from application.models import *


@app.route('/add_product', methods=['POST'])
@login_required
def add_product():
    if current_user.is_admin:
        if request.method == 'POST':
            name = request.form['name']
            description = request.form['description']
            mgf_date = request.form['mgf_date']
            exp_date = request.form['exp_date']
            quantity = request.form['quantity']
            if mgf_date >= exp_date:
                flash(f'mgf date: {mgf_date} and exp date: {exp_date}. The exp date should later than mgf date')
                return redirect(url_for('dashboard_admin'))
            price = request.form['price']
            myfile = request.form['myfile']
            view_type = request.form['view_type']
            category_id = request.form['category_id']
            product=Product(
                name=name,
                img_name = myfile,
                mgf_date = mgf_date,
                exp_date = exp_date,
                quantity = quantity,
                price=price,
                view_type=view_type,
                description = description,
                category_id=int(category_id)
            )
            if product:
                db.session.add(product)
                db.session.commit()
                flash("product created in the database.")
                return redirect(url_for('dashboard_admin'))
    else:
        return "No permission"

@app.route('/add_product/update/<int:id>', methods=['POST'])
@login_required
def add_product_update(id):
    if current_user.is_admin:
        if request.method == 'POST':
            product = Product.query.filter_by(id=id).first()
            if product:
                name = request.form['name']
                description = request.form['description']
                mgf_date = request.form['mgf_date']
                exp_date = request.form['exp_date']
                quantity = request.form['quantity']
                if mgf_date >= exp_date:
                    flash(f'mgf date: {mgf_date} and exp date: {exp_date}. The exp date should later than mgf date')
                    return redirect(url_for('dashboard_admin'))
                price = request.form['price']
                myfile = request.form['myfile']
                view_type = request.form['view_type']
                category_id = request.form['category_id']
                product.name=name
                product.description=description
                product.mgf_date=mgf_date
                product.exp_date=exp_date
                product.price=price
                product.quantity=quantity
                if myfile:
                    product.img_name=myfile
                if view_type:
                    product.view_type=view_type
                if category_id:
                    product.category_id = category_id
                db.session.commit()
                flash(f'The product update to {name}!')
                return redirect(url_for('dashboard_admin'))
            else:
                flash("Something went wrong while updating the product.")
                return redirect(url_for('dashboard_admin'))
    else:
        return "No permission"
        
@app.route('/add_product/delete/<int:id>')
@login_required
def add_product_delete(id):
    if current_user.is_admin:
        product=None
        product = Product.query.filter_by(id=id).first()
        name = product.name
        if product:
            db.session.delete(product)
            db.session.commit()
            flash(f'{name} product deleted')
            return redirect(url_for('dashboard_admin'))
        else:
            flash("Something went wrong while deleting the category.")
            return redirect(url_for('dashboard_admin'))
    else:
        return "No permission"