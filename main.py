from flask import Flask, render_template
from database import db
from models import Product

def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.sqlite3"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)
    app.app_context().push()
    db.create_all()
    return app


app = create_app()


@app.route("/")
def hello_world():
    return render_template("index.html")


@app.route("/myprofile")
def my_profile():
    return render_template("profile.html")


@app.route("/about")
def about():
    return render_template("about.html")


if __name__ == "__main__":
    app.run(debug=True)
