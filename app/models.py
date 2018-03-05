from app import db

class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	gender = db.Column(db.String(10), index=True)
	hasName = db.Column(db.String, index=True)
	ageWeeks = db.Column(db.String, index=True)
	animal = db.Column(db.String, index=True)
	isMix = db.Column(db.String, index=True)
	month = db.Column(db.String, index=True)
	weekday = db.Column(db.String, index=True)
	hourOfDay = db.Column(db.String, index=True)
	isFixed = db.Column(db.String, index=True)
	newBreed = db.Column(db.String(100), index=True)
	newColor = db.Column(db.String(100), index=True)
	outcome = db.Column(db.String(100), index=True)
	
	def __repr__(self):
		return '<ID {}>'.format(self.outcome)