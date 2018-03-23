from app import db
import logging

# Create logging file if DNE otherwise append to it
logging.basicConfig(filename="./app/logs/app.log", level=logging.INFO)

# Create a table in the database provided as the 'SQLALCHEMY_DATABASE_URI' in config.py
# Schema defined in app/models.py
db.create_all()

logging.info('Database created.')
print("DB created.")
