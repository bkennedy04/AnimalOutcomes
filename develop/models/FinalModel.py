import os
import pandas as pd
import numpy as np
import math
from sklearn.ensemble import RandomForestClassifier
import pickle

def fit_randomforest(x_train, y_train, max_features="auto", num_trees=500, SEED=12345):
    """returns trained random forest model

    :param x_train: predictor variable dataframe that has been transformed into suitable format
    :param y_train: response variable dataframe
    :type arg1: pandas dataframe
    :type arg2: pandas dataframe
    :returns: fitted random forest model

    """
    model = RandomForestClassifier(n_estimators=num_trees, max_features=max_features, random_state=SEED)
    model.fit(x_train, y_train)
    
    return model

def prepare_data(train, categorical):
    """returns transformed dataframe, suitable for input in a predictive model

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
	#read in processed data and format
	train = pd.read_csv('..\\data\\processed\\trainset.csv')
	categorical = ['gender', 'weekday', 'newBreed', 'newColor'] 
	train_binary_dummy = prepare_data(train, categorical)
	#train model
	y_train = train_binary_dummy['OutcomeType']
	x_train = train_binary_dummy.drop('OutcomeType', axis=1)
	model_rf = fit_randomforest(x_train, y_train)
	
	#save trained model as pickle for later use
	filename = 'model_v1.pk'
	with open(''+filename, 'wb') as file:
		pickle.dump(model_rf, file)



