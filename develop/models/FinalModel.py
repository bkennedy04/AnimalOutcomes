import os
import pandas as pd
import numpy as np
import math
from sklearn.ensemble import RandomForestClassifier
import pickle

def fit_randomforest(x_train, y_train, max_features="auto"):
    num_trees = 500
    SEED = 12345
    model = RandomForestClassifier(n_estimators=num_trees, max_features=max_features, random_state=SEED)
    model.fit(x_train, y_train)
    
    return model

def prepare_data(train):
	categorical = ['gender', 'weekday', 'newBreed', 'newColor'] 
	# Convert data type as 'category'
	train_binary = train.copy()
	test_binary = test.copy()
	for i in categorical:
		train_binary[i] = train_binary[i].astype('category')
		test_binary[i] = test_binary[i].astype('category')
	# Create dummy variables
	train_binary_dummy = pd.get_dummies(train_binary, columns = categorical)

	return train_binary_dummy

if __name__ == "__main__":
	#read in processed data and format
	train = pd.read_csv('..\\data\\processed\\trainset.csv')
	train_binary_dummy = prepare_data(train)
	#train model
	y_train = train_binary_dummy['OutcomeType']
	x_train = train_binary_dummy.drop('OutcomeType', axis=1)
	model_rf = fit_randomforest(x_train, y_train)
	
	#save model as pickle for later use
	filename = 'model_v1.pk'
	with open(''+filename, 'wb') as file:
		pickle.dump(model_rf, file)




