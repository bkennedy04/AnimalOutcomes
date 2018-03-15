from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# config
app.config.from_object(Config)

# Initialize the database
db = SQLAlchemy(app)

from app import routes

if __name__ == '__main__':
  app.run()