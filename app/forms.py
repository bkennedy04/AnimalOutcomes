from flask_wtf import FlaskForm
from wtforms import SelectField, RadioField, StringField, DecimalField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired

class DataForm(FlaskForm):
	gender = SelectField('Gender of animal:', choices=[('m','Male'), ('f','Female'), ('u','Unknown')])
	hasName = RadioField('Does the animal have a name?', choices=[(1,'yes'), (0,'no')])
	ageWeeks = IntegerField('Age in weeks:', validators=[DataRequired()])
	animal = SelectField('Type of animal:', choices=[(1,'dog'),(0,'cat')])
	isMix = RadioField('Is the animal a mix?', choices=[(1,'yes'), (0,'no')])
	month = SelectField('Month brought to shelter:', choices=[(1,'Jan'),(2,'Feb'),(3,'Mar'),(4,'Apr'),(5,'May'),(6,'June'),(7,'Jul'),(8,'Aug'),(9,'Sep'),(10,'Oct'),(11,'Nov'),(12,'Dec')])
	weekday = SelectField('Day of week brought to shelter:', choices=[(1,'Sunday'),(2,'Monday'),(3,'Tuesday'),(4,'Wednesday'),(5,'Thursday'),(6,'Friday'),(7,'Saturday')])
	hourOfDay = SelectField('Hour of day brought to shelter:', choices=[(0,'12am'),(1,'1am'),(2,'2am'),(3,'3am'),(4,'4am'),(5,'5am'),(6,'6am'),(7,'7am'),(8,'8am'),(9,'9am'),(10,'10am'),(11,'11am'),(12,'12pm'),(13,'1pm'),(14,'2pm'),(15,'3pm'),(16,'4pm'),(17,'5pm'),(18,'6pm'),(19,'7pm'),(20,'8pm'),(21,'9pm'),(22,'10pm'),(23,'11pm')])
	isFixed = RadioField('Is the animal fixed?', choices=[(1,'yes'),(0,'no')])]
	#breed =
	#color
	submit = SubmitField('Submit')