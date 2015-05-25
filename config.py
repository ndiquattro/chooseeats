import os
import csv

WTF_CSRF_ENABLED = True
with open('codes.csv', 'rb') as csvfile:
    codesf = csv.DictReader(csvfile)
    for row in codesf:
        codes = row
SECRET_KEY = codes['secret2']

# Database set-up
basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')