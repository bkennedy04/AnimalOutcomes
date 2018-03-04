from flask import render_template, request, flash, redirect, url_for
from app import app, db
from app.forms import DataForm
from app.models import User
import pandas as pd
import numpy as np
import sys
import os
from src.models import predict_model

@app.route('/')
@app.route('/index')
def index():
	return render_template('index.html')
	
@app.route('/form', methods=['Get', 'POST'])
def form():
	form = DataForm()
	if form.validate_on_submit():
		#user = User(gender=form.gender.data, hasName=form.hasName.data, ageWeeks=form.ageWeeks.data, animal=form.animal.data, isMix = form.isMix.data, month = form.month.data, weekday = form.weekday.data, hourOfDay = form.hourOfDay.data, isFixed = form.isFixed.data)
		#db.session.add(user)                                                                                                  
		#db.session.commit()  
		
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

		app.logger.error(set(test.columns))
		app.logger.error(set(test.columns))

		predicted = pd.DataFrame(model.predict_proba(test))

		
		predicted.columns = ['Adoption', 'Died', 'Euthanasia', 'Return_to_owner', 'Transfer']
		
		return render_template('index.html', adoption=predicted.Adoption, died=predicted.Died, euthanasia=predicted.Euthanasia, return_to_owner=predicted.Return_to_owner, transfer=predicted.Transfer)                                                                               
	return render_template('form.html', title='Enter Data', form=form)                                                        