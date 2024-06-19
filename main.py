from flask import Flask, render_template
from application.database import db
from application.models import *
from flask_login import LoginManager
from werkzeug.security import generate_password_hash, check_password_hash


login_manager = LoginManager()


# I will explain later
@login_manager.user_loader
def load_user(id):
    return User.query.filter_by(id=id).first()


def create_app():
    app = Flask(__name__)
    app.secret_key = 'jjirfar45uqlga@35qkmf'
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.sqlite3"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)
    login_manager.init_app(app)
    app.app_context().push()
    db.create_all()
    if not User.query.filter_by(username="admin").first():
        user = User(username="admin", email="admin@gmail.com", password=generate_password_hash("password"), is_admin=1, total_value=0)
        db.session.add(user)
        db.session.commit()
    return app


app = create_app()
from application.userControllers import *

if __name__ == "__main__":
    app.run(debug=True)
