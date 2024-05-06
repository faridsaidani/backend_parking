from pymongo import MongoClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Vehicule as VehiculeSQL
from dotenv import load_dotenv
import os

load_dotenv()

user = os.environ.get('DB_USER')
password = os.environ.get('DB_PASSWORD')
dbName = os.environ.get('DB_NAME')
mongo_db = os.environ.get('MONGO_DB')
mongo_host = os.environ.get('MONGO_HOST')
mongo_port = int(os.environ.get('MONGO_PORT'))

mongo_client = MongoClient(f'mongodb://{mongo_host}:{mongo_port}/')
mongo_db = mongo_client[mongo_db]
mongo_collection = mongo_db['Vehicule']

engine = create_engine('mysql://{user}:{password}@localhost/{dbName}')
Session = sessionmaker(bind=engine)
session = Session()

# Fetch data from MongoDB
for document in mongo_collection.find():
    # Transform MongoDB document into SQL data
    vehicule = VehiculeSQL(
        numero_immatriculation=document.get('numero_immatriculation'),
        marque=document.get('marque'),
        modele=document.get('modele'),
        couleur=document.get('couleur'),
        annee=document.get('annee'),
        photos=document.get('photos'),
        propietaire=document.get('propietaire'),
    )
    # Insert data into SQL
    session.add(vehicule)

session.commit()