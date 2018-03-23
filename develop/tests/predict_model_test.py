from src.models.predict_model import load_columns, load_model, prepare_data, predict_probs
import pandas as pd
import sklearn.ensemble

# Read in data
data = pd.read_csv('../data/processed/testset.csv')
categorical = ['gender', 'hasName', 'isDog', 'isMix', 'month', 'weekday', 'hourOfDay', 'isFixed', 'newBreed', 'newColor']

def test_prepare_data():
    """Test result of prepare_data"""
    myresult = prepare_data(data, categorical)
    assert type(myresult) is pd.core.frame.DataFrame
    assert myresult.shape == (11456, 113)
    

def test_load_columns():
    """Test result of load_columns"""
    myresult = load_columns()
    assert type(myresult) is pd.core.indexes.base.Index
    assert myresult.shape == (113,)
    
def test_load_model():
    """Test result of load_model"""
    myresult = load_model()
    assert type(myresult) is sklearn.ensemble.forest.RandomForestClassifier
    
def test_predict_probs():
    """Test result of predict_probs"""
    test_binary_dummy = prepare_data(data, categorical)
    model = load_model()
    myresult = predict_probs(test_binary_dummy, model)
    assert type(myresult) is pd.core.frame.DataFrame
    assert myresult.shape == (11456, 5)

