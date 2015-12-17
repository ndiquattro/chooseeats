from app import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(64), index=True, unique=False)
    lastname = db.Column(db.String(64), index=True, unique=False)
    userid = db.Column(db.Integer, index=True, unique=True)
    token = db.Column(db.String(120), index=True, unique=True)

    def __repr__(self):
        return '<User %r>' % self.firstname

    @staticmethod
    def add_user(uinfo):
        # newu = User(uinfo)
        db.session.add(User(**uinfo))
        db.session.commit()

    @staticmethod
    def lookup_user(uid):
        return User.query.filter_by(userid=uid).first()

    @staticmethod
    def users_list():
        # Query DB
        ausers = User.query.with_entities(User.userid)

        # Return list
        return [uid[0] for uid in ausers]
