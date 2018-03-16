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
    with gzip.open(os.path.dirname(__file__)+"./"+path+"/model_v1.pk.gz", "rb") as input_file:
        model_rf = joblib.load(input_file)
    input_file.close()

    return model_rf


def test(data, model):
    """ Returns data frame of probabilities after predicting on trained model

    :param data: test data set to predict on
    :param model: trained model to use to predict test set outcomes
    :type arg1: pandas dataframe
    :type arg2: trained model
    :returns: dataframe of probabilities

    """
    predicted = pd.DataFrame(model.predict_proba(test_binary_dummy))
    predicted.columns = ['Adoption', 'Died', 'Euthanasia', 'Return_to_owner', 'Transfer']

    return predicted.reset_index()


def prepare_data(train, categorical):
    """ Returns transformed dataframe, suitable for input in a predictive model

    :param train: dataframe containing response and predictor variables for predictive model
    :param categoriacl: list of column names needed to be transformed to category type
    :type arg1: pandas dataframe
    :type arg2: list
    :returns: transformed dataframe

    """
    # Convert data type as 'category'
    train_binary = train.copy()
    for i in categorical:
        train_binary[i] = train_binary[i].astype('category')
    # Create dummy variables
    train_binary_dummy = pd.get_dummies(train_binary, columns = categorical)

    return train_binary_dummy


if __name__ == "__main__":

    # Create logging file if DNE otherwise append to it
    logging.basicConfig(filename="../../logs/predict.log", level=logging.INFO)

    # Read in test data set and format
    test = pd.read_csv('../../data/processed/testset.csv')
    logging.info("Test data loaded.")
    categorical = ['gender', 'hasName', 'isDog', 'isMix', 'month', 'weekday', 'hourOfDay', 'isFixed', 'newBreed', 'newColor']
    test_binary_dummy = prepare_data(test, categorical)
    logging.info("Data transformed for prediction.")
    test_binary_dummy.drop('OutcomeType', axis=1, inplace=True)
    model = load_model()
    logging.info("Trained model loaded.")
    # results = test(test_binary_dummy, model) # gives dataframe not callable error
    predicted = pd.DataFrame(model.predict_proba(test_binary_dummy))
    logging.info('Prediction successful.')
    predicted.columns = ['Adoption', 'Died', 'Euthanasia', 'Return_to_owner', 'Transfer']
    print(predicted)

