from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from .auth import auth

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

from app import views, models

# Blueprints
app.register_blueprint(auth, url_prefix='/auth')
