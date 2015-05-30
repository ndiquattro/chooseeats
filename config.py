import os
import csv

WTF_CSRF_ENABLED = True
with open('/home/nickof4/codes.csv', 'rb') as csvfile:
    codesf = csv.DictReader(csvfile)
    for row in codesf:
        codes = row
SECRET_KEY = codes['secret2']

# Database set-up
basedir = os.path.abspath(os.path.dirname(__file__))

#if os.environ.get('DATABASE_URL') is None:
#    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
#else:
SQLALCHEMY_DATABASE_URI = 'mysql://nickof4:mongotut@mysql.server/nickof4$ceatsdb'

SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
