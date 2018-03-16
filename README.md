Animal Outcomes
==============================

Flask web app to predict shelter animal outcomes using Random Forest.

Project Organization
------------
	├── app	                			<- Files for developing flask app
	│   ├── logs					<- Logs generated during use of web app 
	│   ├── static      				<- Static files for flask app to reference
	│   └── templates				<- Dynamic HTML files for flask app use
	│
	├── develop          				<- Files for developing predictive model	
	│	├── data				<- Data files
	│	│   ├── external    			<- The original datasets downloaded from kaggle
	│	│   └── processed   			<- The final, transformed canonical data sets for modeling
	│	│			
	│	├── docs            			<- A default Sphinx project; see sphinx-doc.org for details
	│	│			
	│	├── logs				<- Log files generated during development
	│	│
	│	├── models            	 		<- Trained and serialized models to use for model predictions
	│	│    ├── model_v1.pk.gz			<- Compressed joblib pickle model
	│	│    └── train_columns.pk		<- Pickle of training set columns needed for prediction
	│	│
	│	├── notebooks          			<- Jupyter notebooks and R markdown. Naming convention is a number (for 
	│	│						ordering), the creator's initials, and a short `-` delimited
	│	│						description, e.g. `1.0-jqp-initial-data-exploration`.
	│	│
	│	├── references        	 		<- Data dictionaries, manuals, and all other explanatory materials.
	│	│
	│	├── src                			<- Source code for use in this project
	│	│    ├── __init__.py    		<- Makes src a Python module
	│	│    │ 
	│	│    ├── features      			<- Scripts to turn raw data into features for modeling
	│	│    │   └── build_features.R		<- R script to read in external data, build features, and export processed data
	│	│    │
	│	│    └── models         		<- Scripts to train models and then use trained models to make predictions
	│	│        │   
	│ 	│ 	 ├── __init__.py    		<- Makes models a Python module
	│	│        ├── predict_model.py		<- Functionality to load serialized model and model columns
	│	│        └── train_model.py     	<- Trains and serializes model
	│	│ 
	│ 	├── tests				<- Unit tests
	│ 	├── __init__.py    			<- Makes develop a Python module
	│	└── .gitignore	
	│
	├── application.py              		<- Flask app setup       
	├── db_create.py             			<- Script to create database 
	├── README.md              			<- Top level readme
	├── requirements.txt            		<- The requirements file for reproducing the analysis environment, e.g.
	│	                      	   			generated with `pip freeze > requirements.txt`
	├── __init__.py              			<- Makes root directory a Python module
	└── .gitignore					
	
Suggested Steps	to Reproduce	
--------

1. Clone AnimalOutcomes repository.

2. Download data from [here](https://www.kaggle.com/c/shelter-animal-outcomes/data) and extract and save in AnimalOutcomes/develop/data/external as 'train.csv' and 'test.csv'.

3. Create conda environment. 

    `conda create -n myenv python=3`
    
4. Activate environment.

    `source activate myenv`
	
   Windows Users:

    `activate myenv`

5. Install required packages. 

    `pip install -r requirements.txt`

6. Navigate to AnimalOutcomes/develop/src/features and run build_features.R script. This will process the external data and export to AnimalOutcomes/develop/data/processed.

	`Rscript build_features.R`
	
7. Navigate to AnimalOutcomes/develop/src/models and run train_model.py. This will train random forest model using processed data and serialize model for later use.

	`python train_model.py`
	
8. Now run predict_model.py to make sure everything is working as expected.

	`python predict_model.py`
	
9. Navigate to AnimalOutcomes/ and create a config.py file with the information necessary to create your database connection. **Do not commit this file.** 
     
    ```python
	import os
	basedir = os.path.abspath(os.path.dirname(__file__))

	class Config(object):
		SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
		SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'app.db')
		# If using AWS RDS fill in line below and replace line above.
		# SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://<user>:<password>@<endpoint>/<database name>'
		SQLALCHEMY_TRACK_MODIFICATIONS = False
    ``` 
10. Create the database.

	`python db_create.py`
	
11. You are now ready to run the flask app.

	`python application.py`

--------

<p><small>Project based on the <a target="_blank" href="https://drivendata.github.io/cookiecutter-data-science/">cookiecutter data science project template</a>. #cookiecutterdatascience</small></p>
