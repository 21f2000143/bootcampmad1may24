from application.orderControllers import *
from application.userControllers import *
from application.proControllers import *
from application.catControllers import *
from flask import Flask, render_template
from flask_login import LoginManager
import os
from application.models import *
from application.config import LocalDevelopmentConfig
from werkzeug.security import generate_password_hash
from flask_restful import Resource, Api


login_manager = LoginManager()


@login_manager.user_loader
def load_user(id):
    return User.query.filter_by(id=id).first()


app = None


def create_app():
    app = Flask(__name__)
    if os.getenv('ENV', "development") == "production":
        raise Exception("Currently no production config is setup.")
    else:
        app.config.from_object(LocalDevelopmentConfig)

    db.init_app(app)
    app.app_context().push()
    api = Api(app)
    login_manager.init_app(app)
    app.app_context().push()
    db.create_all()
    admin = User.query.filter_by(is_admin=1).first()
    if not admin:
        admin = User(username='admin', email='admin@gmail.com',
                     password=generate_password_hash('password'),
                     is_admin=1, total_value=0)
        db.session.add(admin)
        db.session.commit()
    return app, api


app, api = create_app()


@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('404.html'), 404


from application.apiResources import productApi


api.add_resource(productApi, '/api/products', '/api/products/<int:product_id>')
# importing all the controllers here

if __name__ == '__main__':
    app.run(debug=True)
