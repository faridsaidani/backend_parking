import json
import os
import mysql.connector
from pymongo import MongoClient
from dotenv import load_dotenv
from bson import json_util


load_dotenv()
# SQL Configuration
db_user = os.environ.get('DB_USER')
db_password = os.environ.get('DB_PASSWORD')
db_name = os.environ.get('DB_NAME')
db_host = os.environ.get('DB_HOST')
cnx = mysql.connector.connect(user=db_user, password=db_password,
                              host=db_host, database=db_name)

cursor = cnx.cursor()

# MongoDB Configuration
mongo_db = os.environ.get('MONGO_DB')
mongo_host = os.environ.get('MONGO_HOST')
mongo_port = int(os.environ.get('MONGO_PORT'))  # convert to int because port should be a number

client = MongoClient(f'mongodb://{mongo_host}:{mongo_port}/')

db = client[mongo_db]
mongo_collection = db['vehicule']

# Exporting MongoDB data to JSON file
with open('mongo_data.json', 'w') as f:
    json.dump(list(mongo_collection.find()), f, default=json_util.default)

cursor.execute("""
    CREATE TABLE IF NOT EXISTS vehicule (
        _id VARCHAR(255),
        numero_immatriculation VARCHAR(20),
        marque VARCHAR(255),
        modele VARCHAR(255),
        couleur VARCHAR(255),
        annee INT,
        photos TEXT,
        propietaire INT,
        FOREIGN KEY (propietaire) REFERENCES utilisateur(id)
    )
""")

with open('mongo_data.json', 'r') as f:
    data = json.load(f)

for record in data:
    record["_id"]["$oid"] = record["_id"]["$oid"]
    record["numero_immatriculation"] = str(record["numero_immatriculation"])
    record["marque"] = str(record["marque"])
    record["modele"] = str(record["modele"])
    record["couleur"] = str(record["couleur"])
    record["annee"] = int(record["annee"])
    record["photos"] = str(record["photos"])
    record["propietaire"] = int(record["propietaire"])

    cursor.execute("""
        INSERT INTO vehicule (_id, numero_immatriculation, marque, modele, couleur, annee, photos, propietaire)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
    """, (record["_id"]["$oid"], record["numero_immatriculation"], record["marque"], record["modele"], record["couleur"], record["annee"], record["photos"], record["propietaire"]))

cnx.commit()
cnx.close()
print("Data migrated successfully from MongoDB to MySQL.")