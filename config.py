import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
	SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
	SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'app.db')
	#SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://animaloutcomes:Desktop01@animaloutcomesdatabase.c76qrkgxophn.us-east-1.rds.amazonaws.com/animaldb'
	SQLALCHEMY_TRACK_MODIFICATIONS = False 
	
	
	