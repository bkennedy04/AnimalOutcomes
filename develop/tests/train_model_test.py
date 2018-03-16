from src.models.train_model import prepare_data, fit_randomforest
import pandas as pd
import sklearn.ensemble

# Read in data
data = pd.read_csv('../data/processed/trainset.csv')
categorical = ['gender', 'hasName', 'isDog', 'isMix', 'month', 'weekday', 'hourOfDay', 'isFixed', 'newBreed', 'newColor']

def test_prepare_data():
    """Test result of prepare_data"""
    myresult = prepare_data(data, categorical)
    assert type(myresult) is pd.core.frame.DataFrame
    assert myresult.shape == (26728, 114)
    

def test_fit_randomforest():
    """Test result of prepare_data"""
    dat = prepare_data(data, categorical)
    y_train = dat['OutcomeType']
    x_train = dat.drop('OutcomeType', axis=1)
    myresult = fit_randomforest(x_train, y_train)
    assert type(myresult) is sklearn.ensemble.forest.RandomForestClassifier
