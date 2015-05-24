#!flask/bin/python
from app import db, models

users = models.User.query.all()
for u in users:
    db.session.delete(u)
    
db.session.commit()