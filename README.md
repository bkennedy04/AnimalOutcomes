Animal Outcomes
==============================

Web app to predict shelter animal outcomes. You can download the original dataset [here](https://www.kaggle.com/c/shelter-animal-outcomes/data).

Project Organization
------------
	├── app	                       		<- Files for developing flask app
	│   ├── static      
	│   └── templates
	└── develop          	       		<- Files for developing predictive model
		|
		├── Makefile           		<- Makefile with commands like `make data` or `make train`
		├── data
		│   ├── external       		<- The original datasets downloaded from kaggle
		│   └── processed      		<- The final, transformed canonical data sets for modeling
		│   
		│
		├── docs               		<- A default Sphinx project; see sphinx-doc.org for details
		│
		├── models            	 	<- Trained and serialized models to use for model predictions
		│    ├── model_v1.pk.gz		<- Compressed joblib pickle model
		|    └── train_columns.pk	<- Pickle of training set columns needed for prediction
		|
		├── notebooks          		<- Jupyter notebooks. Naming convention is a number (for ordering),
		│                         	   the creator's initials, and a short `-` delimited description, e.g.
		│                         	   `1.0-jqp-initial-data-exploration`.
		│
		├── references        	 	<- Data dictionaries, manuals, and all other explanatory materials.
		│
		├── requirements.txt   		<- The requirements file for reproducing the analysis environment, e.g.
		│                         	   generated with `pip freeze > requirements.txt`
		│
		├── src                		<- Source code for use in this project
		    ├── __init__.py    		<- Makes src a Python module
		    │
		    ├── data         		<- Scripts to download or generate data
		    │   └── make_dataset.py
		    │ 
		    ├── features      		 <- Scripts to turn raw data into features for modeling
		    │   └── build_features.R	 <- R script to read in external data, build features, and export processed data
		    │
		    └── models         		<- Scripts to train models and then use trained models to make predictions
		        │                 
		        ├── predict_model.py	<- Functionality to load serialized model and model columns
		        └── train_model.py      <- Trains and serializes model
		
		


--------

<p><small>Project based on the <a target="_blank" href="https://drivendata.github.io/cookiecutter-data-science/">cookiecutter data science project template</a>. #cookiecutterdatascience</small></p>
