import pandas as pd
import pickle
import os


def load_columns(path='./'):
	"""returns list of training set columns to validate against test set

	:returns: training set columns

	"""
	with open(os.path.dirname(__file__)+"\\train_columns.pk", "rb") as input_file:
		train_columns = pickle.load(input_file)
	
	return train_columns

def load_model(path='./'):
	"""returns trained model loaded in from pickle file

	:returns: training model

	"""
	with open(os.path.dirname(__file__)+"\\model_v1.pk", "rb") as input_file:
		model_rf = pickle.load(input_file)
	
	return model_rf

def test(data, model):
	"""returns data frame of probabilities after predicting on trained model

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
	#read in test data and format
	test = pd.read_csv('..\\..\\data\\processed\\testset.csv')
	categorical = ['gender', 'hasName', 'isDog', 'isMix', 'month', 'weekday', 'hourOfDay', 'isFixed', 'newBreed', 'newColor']  
	test_binary_dummy = prepare_data(test, categorical)
	test_binary_dummy.drop('OutcomeType', axis=1, inplace=True)
	model = load_model()
	#results = test(test_binary_dummy, model)
	predicted = pd.DataFrame(model.predict_proba(test_binary_dummy))
	predicted.columns = ['Adoption', 'Died', 'Euthanasia', 'Return_to_owner', 'Transfer']

