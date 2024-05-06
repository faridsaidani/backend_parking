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

table_utilisateur = "utilisateur"
table_facture = "facture"
table_entree_sortie = "entree__sortie"

cursor.execute("""
    SELECT * FROM utilisateur
""")
utilisateurs = cursor.fetchall()

# Get column names from cursor description
column_names = [column[0] for column in cursor.description]

for utilisateur in utilisateurs:
    # Convert tuple to dictionary
    utilisateur_dict = dict(zip(column_names, utilisateur))

    mongo_collection = db['utilisateur']
    mongo_collection.insert_one(utilisateur_dict)


cursor.execute("""
               SELECT* FROM facture
""")
factures = cursor.fetchall()
column_names = [column[0] for column in cursor.description]

for facture in factures:
    factures_dict = dict(zip(column_names, facture))
    mongo_collection = db['factures']
    mongo_collection.insert_one(factures_dict)

cursor.execute("""
               SELECT* FROM entree__sortie
""")
entree_sorties = cursor.fetchall()
column_names = [column[0] for column in cursor.description]

for es in entree_sorties:
    factures_dict = dict(zip(column_names, es))
    mongo_collection = db['entree__sortie']
    mongo_collection.insert_one(factures_dict)



print("Inserted successfully")