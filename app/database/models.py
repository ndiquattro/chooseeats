from app import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(64), index=True, unique=False)
    lastname = db.Column(db.String(64), index=True, unique=False)
    userid = db.Column(db.Integer, index=True, unique=True)
    token = db.Column(db.String(120), index=True, unique=True)
    friends = db.relationship('Friends', backref='prime', lazy='dynamic')

    def __repr__(self):
        return '<User %r>' % self.firstname


class Friends(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fuid = db.Column(db.Integer, index=True, unique=False)
    primeid = db.Column(db.Integer, db.ForeignKey('user.id'))
