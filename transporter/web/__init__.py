from flask import Flask, render_template
from flask.ext.sqlalchemy import SQLAlchemy
from transporter import settings
from transporter.web.http_basic_auth import requires_auth


app = Flask(__name__, static_folder='public', static_url_path='/public')

@app.route("/")
@requires_auth
def index():
    return render_template('index.html')
