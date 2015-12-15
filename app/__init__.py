from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

# Initiate Flask
app = Flask(__name__)
app.config.from_object('config')

# Connect to database
db = SQLAlchemy(app)

# Import Blueprints
from .views.home import home
from .views.auth import auth
from .views.results import results

# Blueprints
app.register_blueprint(home)
app.register_blueprint(auth)
app.register_blueprint(results)

# Final Import
from app import views
