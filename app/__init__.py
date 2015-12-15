from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

from .auth import auth
from .results import results
from app import views, models

# Blueprints
app.register_blueprint(auth, url_prefix='/auth')
app.register_blueprint(results, url_prefix='/results')
