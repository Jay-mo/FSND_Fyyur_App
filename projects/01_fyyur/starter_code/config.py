import os
SECRET_KEY = os.urandom(32)
# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

# Enable debug mode.
DEBUG = True

# Connect to the database

database_name = "fyyur_db"
database_username = os.getenv('DBUSER')
database_password = os.getenv('DBPASS')
# TODO IMPLEMENT DATABASE URL'
SQLALCHEMY_DATABASE_URI = "postgresql://{}:{}@{}/{}".format(database_username, database_password,'localhost:5432', database_name)

SQLALCHEMY_TRACK_MODIFICATIONS = False




