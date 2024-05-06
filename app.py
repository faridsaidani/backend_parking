from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_mongoengine import MongoEngine
from dotenv import load_dotenv
import os
from flask_cors import CORS

load_dotenv()

app = Flask(__name__)
CORS(app)
# set the secret key from environment variable
app.secret_key = os.environ.get('SECRET_KEY')

# get user and password from environment variables
user = os.environ.get('DB_USER')
password = os.environ.get('DB_PASSWORD')
dbName = os.environ.get('DB_NAME')
db_host = os.environ.get('DB_HOST')

# MySQL Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql://{user}:{password}@{db_host}/{dbName}'


# MySQL Configuration
db = SQLAlchemy(app)


# MongoDB Configuration
mongo_db = os.environ.get('MONGO_DB')
mongo_host = os.environ.get('MONGO_HOST')
mongo_port = int(os.environ.get('MONGO_PORT'))  # convert to int because port should be a number

# MongoDB Configuration
app.config["MONGODB_SETTINGS"] = {
    "db": mongo_db,
    "host": mongo_host,
    "port": mongo_port
}
mongo = MongoEngine(app)

# Import routes after the database is iset SECRET_KEY=_5#y2L"F4Q8z\n\xec]/
from routes import *

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)