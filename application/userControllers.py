from flask import current_app as app, render_template
from flask_login import login_required


@app.route('/')
@login_required
def index():
    return render_template('index.html')
