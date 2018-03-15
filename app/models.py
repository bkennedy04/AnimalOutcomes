from app import db

# Create database schema
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    gender = db.Column(db.String(10), index=True)
    hasName = db.Column(db.String(100), index=True)
    ageWeeks = db.Column(db.String(100), index=True)
    animal = db.Column(db.String(100), index=True)
    isMix = db.Column(db.String(100), index=True)
    month = db.Column(db.String(100), index=True)
    weekday = db.Column(db.String(100), index=True)
    hourOfDay = db.Column(db.String(100), index=True)
    isFixed = db.Column(db.String(100), index=True)
    newBreed = db.Column(db.String(100), index=True)
    newColor = db.Column(db.String(100), index=True)
    outcome = db.Column(db.String(100), index=True)

    def __repr__(self):
        return '<ID {}>'.format(self.outcome)