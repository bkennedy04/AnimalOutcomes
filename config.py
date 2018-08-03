import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
	SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
	SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'app.db')
	# If using AWS RDS fill in line below and replace line above.
	# SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://<user>:<password>@<endpoint>/<database name>'
	SQLALCHEMY_TRACK_MODIFICATIONS = False
