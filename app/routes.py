from flask import render_template, request, flash, redirect, url_for
from app import app, db
from app.forms import DataForm
from app.models import User
from develop.src.models.train_model import prepare_data
from develop.src.models.predict_model import load_columns, load_model
import pandas as pd
import numpy as np
import logging


# Create logging file if DNE otherwise append to it
logging.basicConfig(filename="./app/logs/app.log", level=logging.INFO)


@app.route('/', methods=['Get', 'POST'])
@app.route('/index', methods=['Get', 'POST'])
def form():
    """ View to process post

    View that displays form and processes user input and predicts
    outcome using serialized random forest model

    :return: rendered html template

    """
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
        logging.info('User input received.')

        # Create data frame of user input
        columns = ['gender','hasName','ageWeeks','isDog','isMix','month','weekday','hourOfDay','isFixed','newBreed','newColor']
        mylist = [gender, hasName, ageWeeks, animal, isMix, month, weekday, hourOfDay, isFixed, newBreed, newColor]
        test = pd.DataFrame(np.array(mylist).reshape(1,11), columns=columns)

        # Prepare data
        categorical = ['gender', 'hasName', 'isDog', 'isMix', 'month', 'weekday', 'hourOfDay', 'isFixed', 'newBreed', 'newColor']
        test_binary_dummy = prepare_data(test, categorical)
        train_columns = load_columns()
        # Get missing columns in the training test
        missing_cols = set( train_columns ) - set( test_binary_dummy.columns )
        # Add missing columns in test set with default value equal to 0
        for c in missing_cols:
            test_binary_dummy[c] = 0
        # Ensure the order of column in the test set is in the same order than in train set
        test = test_binary_dummy[train_columns]

        # Predict using trained model
        model = load_model()
        logging.info('Trained model loaded.')
        predicted = pd.DataFrame(model.predict_proba(test))
        outcome_class = model.predict(test)[0]
        predicted.columns = ['Adoption', 'Died', 'Euthanasia', 'Return_to_owner', 'Transfer']
        logging.info('Predicted outcome using trained model and user input.')

        # Create message to display based on outcome
        message = ''
        alert = ''
        if outcome_class == 'Adoption':
            message += 'Congrats, it looks like adoption is likely! :)'
            alert += 'success'
        elif outcome_class == 'Died':
            message += 'Uh oh, it looks like death is likely :('
            alert += 'danger'
        elif outcome_class == 'Euthanasia':
            message += 'Uh oh, it looks like euthanasia is likely :('
            alert += 'danger'
        elif outcome_class == 'Return_to_owner':
            message += 'Congrats, it looks like returning to owner is likely!'
            alert += 'success'
        else:
            message += 'It looks like transfer is likely.'
            alert += 'warning'

        # Push user input and predicted class to database
        user = User(gender=gender, hasName=hasName, ageWeeks=ageWeeks, animal=animal, isMix=isMix, month=month, weekday=weekday, hourOfDay = hourOfDay, isFixed = isFixed, newBreed=newBreed, newColor=newColor, outcome=outcome_class)
        db.session.add(user)
        db.session.commit()
        logging.info('User input and prediction commited to database.')

        return render_template('index.html', adoption=round(predicted.iloc[0]['Adoption'], 4), died=round(predicted.iloc[0]['Died'], 4), euthanasia=round(predicted.iloc[0]['Euthanasia'], 4), return_to_owner=round(predicted.iloc[0]['Return_to_owner'], 4), transfer=round(predicted.iloc[0]['Transfer'], 4), message=message, alert=alert)
    return render_template('form.html', title='Enter Data', form=form)


@app.route('/about')
def about():
    """ View that renders pdf

    :return: Rendered html template

    """
    logging.info('User visited the about page.')
    return render_template('about.html')