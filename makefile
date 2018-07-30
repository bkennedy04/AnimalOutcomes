develop/data/processed/trainset.csv: develop/data/external/train.csv
	Rscript develop/data/processed/build_features.R

develop/models/model_v1.pk.gz: develop/data/processed/trainset.csv
	python develop/src/models/train_model.py


model: develop/models/model_v1.pk.gz

app.db: model
	python db_create.py

all: app.db model
	python application.py