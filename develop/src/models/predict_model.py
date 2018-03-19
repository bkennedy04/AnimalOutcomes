import pandas as pd
import pickle
import os
from sklearn.externals import joblib
import gzip
import logging


def load_columns(path='../../models/'):
    """ Returns list of training set columns to validate against test set, loaded from pickle file

    :param path: path to pickle file
    :returns: training set columns

    """
    with open(os.path.dirname(__file__)+"/"+path+"/train_columns.pk", "rb") as input_file:
        train_columns = pickle.load(input_file)
    input_file.close()

    return train_columns


def load_model(path='../../models/'):
    """ Returns trained model loaded in from compressed joblib pickle file

    :param path: path to pickle file
    :returns: training model

    """
    with gzip.open(os.path.dirname(__file__)+"/"+path+"/model_v1.pk.gz", "rb") as input_file:
        model_rf = joblib.load(input_file)
    input_file.close()

    return model_rf


def predict_probs(data, model):
    """ Returns data frame of probabilities after predicting on trained model in a format suitable for submission to kaggle competition

    :param data: test data set to predict on
    :param model: trained model to use to predict test set outcomes
    :type arg1: pandas dataframe
    :type arg2: trained model
    :returns: dataframe of probabilities

    """
    predicted = pd.DataFrame(model.predict_proba(data))
    predicted.columns = ['Adoption', 'Died', 'Euthanasia', 'Return_to_owner', 'Transfer']
    predicted.reset_index()
    predicted.index += 1
    predicted.index.name = 'ID' 
    return predicted


def prepare_data(test, categorical):
    """ Returns transformed dataframe, suitable for input in a predictive model

    :param train: dataframe containing response and predictor variables for predictive model
    :param categorical: list of column names needed to be transformed to category type
    :type arg1: pandas dataframe
    :type arg2: list
    :returns: transformed dataframe

    """
    # Convert data type as 'category'
    test_binary = test.copy()
    for i in categorical:
        test_binary[i] = test_binary[i].astype('category')
    # Create dummy variables
    test_binary_dummy = pd.get_dummies(test_binary, columns = categorical)
    # If there is a column 'OutcomeType', drop it
    if 'OutcomeType' in test_binary_dummy.columns:
        test_binary_dummy.drop('OutcomeType', axis=1, inplace=True)

    return test_binary_dummy


if __name__ == "__main__":

    # Create logging file if DNE otherwise append to it
    logging.basicConfig(filename="../../logs/predict.log", level=logging.INFO)

    # Read in test data set and format
    testdata = pd.read_csv('../../data/processed/testset.csv')
    logging.info("Test data loaded.")
    categorical = ['gender', 'hasName', 'isDog', 'isMix', 'month', 'weekday', 'hourOfDay', 'isFixed', 'newBreed', 'newColor']
    test_binary_dummy = prepare_data(testdata, categorical)
    logging.info("Data transformed for prediction.")
    model = load_model()
    logging.info("Trained model loaded.")
	
	# Create dataframe of predicted probabilities
    results = predict_probs(test_binary_dummy, model)
    logging.info('Prediction successful.')
    print("Predicted probabilities:")
    print(results.head())

