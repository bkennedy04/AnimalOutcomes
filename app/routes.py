from flask import render_template, request, flash, redirect, url_for
from app import app, db
from app.forms import DataForm
from app.models import User
import pandas as pd
import numpy as np
import sys
import os
from develop.src.models import predict_model

@app.route('/results')
def index():
	return render_template('index.html')
	
@app.route('/', methods=['Get', 'POST'])
@app.route('/index', methods=['Get', 'POST'])
def form():
	form = DataForm()
	if form.validate_on_submit():		
		gender=request.form['gender']
		hasName=int(request.form['hasName'])
		ageWeeks=request.form['ageWeeks']
		animal=request.form['animal']
		isMix=request.form['isMix']
		month=request.form['month']
		weekday=request.form['weekday']
		hourOfDay=request.form['hourOfDay']
		isFixed=request.form['isFixed']
		newBreed=request.form['newBreed']
		newColor=request.form['newColor']
		
		#create data frame of user input
		columns=['gender','hasName','ageWeeks','isDog','isMix','month','weekday','hourOfDay','isFixed','newBreed','newColor']
		mylist = [gender, hasName, ageWeeks, animal, isMix, month, weekday, hourOfDay, isFixed, newBreed, newColor]
		test = pd.DataFrame(np.array(mylist).reshape(1,11), columns = columns)
		
		#prepare data
		categorical = ['gender', 'hasName', 'isDog', 'isMix', 'month', 'weekday', 'hourOfDay', 'isFixed', 'newBreed', 'newColor']  
		test_binary_dummy = predict_model.prepare_data(test, categorical)
		train_columns = predict_model.load_columns()
		#get missing columns in the training test
		missing_cols = set( train_columns ) - set( test_binary_dummy.columns )
		#Add missing columns in test set with default value equal to 0
		for c in missing_cols:
			test_binary_dummy[c] = 0
		#Ensure the order of column in the test set is in the same order than in train set
		test = test_binary_dummy[train_columns]
		
		#predict using trained model
		model = predict_model.load_model()
		mycols = set(test.columns).difference(set(train_columns))
		predicted = pd.DataFrame(model.predict_proba(test))
		outcome_class = model.predict(test)
		predicted.columns = ['Adoption', 'Died', 'Euthanasia', 'Return_to_owner', 'Transfer']
		
		probs = [predicted.iloc[0]['Adoption'], predicted.iloc[0]['Died'], predicted.iloc[0]['Euthanasia'], predicted.iloc[0]['Return_to_owner'], predicted.iloc[0]['Transfer']]                                                  
		
		message=''
		alert=''
		if(outcome_class == 'Adoption'):
			message += 'Congrats, it looks like adoption is likely! :)'
			alert += 'success'
		elif(outcome_class == 'Died'):
			message += 'Uh oh, it looks like death is likely :('
			alert += 'danger'
		elif(outcome_class == 'Euthanasia'):
			message += 'Uh oh, it looks like euthanasia is likely :('
			alert += 'danger'
		elif(outcome_class == 'Return_to_owner'):
			message += 'Congrats, it looks like returning to owner is likely!'
			alert += 'success'
		else:
			message += 'It looks like transfer is likely.'
			alert += 'warning'
			
		#push user input and predicted class to database
		user = User(gender=gender, hasName=hasName, ageWeeks=ageWeeks, animal=animal, isMix=isMix, month=month, weekday=weekday, hourOfDay = hourOfDay, isFixed = isFixed, newBreed=newBreed, newColor=newColor, outcome=outcome_class)
		db.session.add(user)                                                                                                                                                                                                                                              
		db.session.commit()                                                                                                                                                                                                                                               
		
		return render_template('index.html', adoption=round(predicted.iloc[0]['Adoption'],4), died=round(predicted.iloc[0]['Died'],4), euthanasia=round(predicted.iloc[0]['Euthanasia'],4), return_to_owner=round(predicted.iloc[0]['Return_to_owner'],4), transfer=round(predicted.iloc[0]['Transfer'],4), message=message, alert=alert)                                                                               
	return render_template('form.html', title='Enter Data', form=form)     

@app.route('/about')
def about():	
	return render_template('about.html')