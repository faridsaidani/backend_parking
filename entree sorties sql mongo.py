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



cursor.execute("""
               SELECT* FROM entree__sortie
""")
entree_sorties = cursor.fetchall()
column_names = [column[0] for column in cursor.description]



for es in entree_sorties:
    factures_dict = dict(zip(column_names[1:], es[1:]))
    mongo_collection = db['entree__sortie']
    mongo_collection.insert_one(factures_dict)


print("Inserted successfully")