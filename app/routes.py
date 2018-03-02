from flask import render_template
from app import app
from app.forms import DataForm

@app.route('/')
@app.route('/index')
def index():
	user = {'username': 'Miguel'}
	return render_template('index.html', title='Home', user=user)
	
@app.route('/form', methods=['Get', 'POST'])
def form():
	form = DataForm()
	if form.validate_on_submit():
		user = User(gender=form.gender.data, hasName=form.hasName.data, ageWeeks=form.ageWeeks.data)
		db.session.add(user)
		db.session.commit()
		return redirect(url_for('index'))
	return render_template('form.html', title='Enter Data', form=form)