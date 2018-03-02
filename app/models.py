from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    gender = db.Column(db.String(10), index=True)
    hasName = db.Column(db.Boolean, index=True)
    ageWeeks = db.Column(db.Integer)

    def __repr__(self):
        return '<ID {}>'.format(self.id)