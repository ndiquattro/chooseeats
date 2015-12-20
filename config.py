import os
import yaml

# Database set-up
basedir = os.path.abspath(os.path.dirname(__file__))

# Switch if on server or local
if os.uname()[0] == 'Darwin':
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
    codepath = 'codes.csv'
else:
    SQLALCHEMY_DATABASE_URI = 'mysql://nickof4:mongotut@mysql.server/nickof4$ceatsdb'
    SQLALCHEMY_POOL_RECYCLE = 280  # Based on pythonanywhere support site
    codepath = '/home/nickof4/codes.csv'

SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')

# Session set-up
WTF_CSRF_ENABLED = True

# API keys setup
with open('secrets.yaml', 'r') as f:
    secrets = yaml.load(f)

FSCL = secrets['fscid']
FSST = secrets['fssct']

# Forms setup
SECRET_KEY = secrets['forms']
