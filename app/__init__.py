from flask import Flask
from animaloutcomes.config import Config
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)

from animaloutcomes.app import routes