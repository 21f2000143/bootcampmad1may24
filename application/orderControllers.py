from flask import current_app as app, request, flash, redirect, url_for, render_template
from flask_login import current_user, login_required, login_user
from application.models import *
from datetime import datetime

@app.route('/orders')
def list_orders():
    orders = Order.query.all()
    return render_template('orders.html', orders=orders)

@app.route('/add_order', methods=['GET', 'POST'])
def add_order():
    if request.method == 'POST':
        user_id = request.form['user_id']
        product_id = request.form['product_id']
        order_date = datetime.now()
        
        order = Order(user_id=user_id, product_id=product_id, order_date=order_date)
        db.session.add(order)
        db.session.commit()
        return redirect(url_for('list_orders'))
    return render_template('add_order.html')

@app.route('/user/add/to/cart/<int:id>')
@login_required
def add_to_cart(id):
    if not current_user.is_admin:
        product = Product.query.filter_by(id=id).first()
        search_item_in_cart = UserProduct.query.filter_by(product_id = int(id), user_id = int(current_user.id)).first()
        if search_item_in_cart:
            if product.quantity > search_item_in_cart.quantity:
                search_item_in_cart.quantity+=1
                db.session.commit()
                current_user.total_value+=product.price
                db.session.commit()
                flash(f"Added one more quantity of the {product.name}")
                return redirect(url_for('dashboard_user'))
            else:
                flash(f"no more quantity is availabe for{product.name}")
                return redirect(url_for('dashboard_user'))
        else:
            add_item_in_cart = UserProduct(product_id=id, user_id= current_user.id, quantity=1)
            db.session.add(add_item_in_cart)
            db.session.commit()
            current_user.total_value+=product.price
            db.session.commit()
            flash(f"{product.name} added into your cart.")
            return redirect(url_for('dashboard_user'))
    else:
        return "No permission"
@app.route('/user/remove/to/cart/<int:id>')
@login_required
def remove_to_cart(id):
    if not current_user.is_admin:
        product = Product.query.filter_by(id=id).first()
        if product:
            search_item_in_cart = UserProduct.query.filter_by(product_id = int(id), user_id = int(current_user.id)).first()
            if search_item_in_cart:
                current_user.total_value-=product.price*search_item_in_cart.quantity
                db.session.commit()
                db.session.delete(search_item_in_cart)
                db.session.commit()
                flash(f"Removed {product.name} from your cart.")
                return redirect(url_for('dashboard_user'))
            else:
                flash(f"{product.name} not in your cart.")
                return redirect(url_for('dashboard_user'))
        else:
            flash(f"Oops! product not there.")
            return redirect(url_for('dashboard_user'))
    else:
        return "No permission"
    
@app.route('/user/payment')
@login_required
def user_payment():
    if not current_user.is_admin:
        search_item_in_cart = UserProduct.query.filter_by(user_id = int(current_user.id)).all()
        for item in current_user.cart:
            for quantity_tuple in search_item_in_cart:
                if quantity_tuple.product_id==item.id:
                    product = Product.query.filter_by(id=item.id).first()
                    product.quantity -= quantity_tuple.quantity
                    db.session.commit()
                    amount = quantity_tuple.quantity * item.price
                    order = Order(current_user.id, name=item.name, img_name=item.img_name, amount=amount, order_date=datetime.now())
                    db.session.add(order)
                    db.session.commit()
        current_user.cart.clear()
        db.session.commit()
        current_user.total_value=0
        db.session.commit()
        flash(f"Thank you for shopping, visit again.")
        return redirect(url_for('dashboard_user'))
    else:
        return "No permission"
