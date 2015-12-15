from app import db
from app.database import models

users = models.User.query.filter_by(firstname='Nick').first()
db.session.delete(users)
# for u in users:
#     db.session.delete(u)
    
db.session.commit()
