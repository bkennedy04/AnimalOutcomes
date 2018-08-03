requirements: requirements.txt
	pip install -r requirements.txt

feature_engineering: develop/data/external/train.csv develop/src/features/build_features.R
	Rscript develop/src/features/build_features.R

modeling: develop/data/processed/trainset.csv develop/models/model_v1.pk.gz develop/models/train_columns.pk
	python develop/src/models/train_model.py

database: app/models.py app/routes.py
	python db_create.py

all: requirements feature_engineering modeling database
	python application.py