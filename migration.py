from pymongo import MongoClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models_sql import Vehicule as VehiculeSQL

# Set up MongoDB connection
mongo_client = MongoClient('mongodb://localhost:27017/')
mongo_db = mongo_client['your_mongodb_database']
mongo_collection = mongo_db['Vehicule']

# Set up SQL connection
engine = create_engine('mysql://username:password@localhost/your_sql_database')
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

# Commit the changes
session.commit()