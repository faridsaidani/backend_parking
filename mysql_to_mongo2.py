import pymysql
import json
import os
import mysql.connector
from pymongo import MongoClient
from dotenv import load_dotenv
from bson import json_util
import datetime


load_dotenv()

 #mongodb connection
mongo_connection_string = os.getenv('MONGO_CONNECTION_STRING')
client= MongoClient(mongo_connection_string)

db = client['contact_manager']
#i created a new collection called mysql_data to store the data from mysql seperately
mongo_collection = db['mysql_data']

#mysql connection
db_user = os.getenv('DB_USER')
db_password = os.getenv('DB_PASSWORD')
db_host = os.getenv('DB_HOST')
db_name = os.getenv('DB_NAME')

cnx = mysql.connector.connect(user=db_user, password=db_password,
                              host=db_host, database=db_name)

cursor = cnx.cursor(dictionary=True)
# Fetch data from MySQL
cursor.execute("SELECT * FROM CONTACTS")
rows = cursor.fetchall()


# Insert data into MongoDB
for row in rows:
    # Convert data to string if necessary
    row['id'] = str(row['id'])
    row['nom'] = str(row['nom'])
    row['prenom'] = str(row['prenom'])
    row['adresse_email'] = str(row['adresse_email'])
    row['numero_telephone'] = str(row['numero_telephone'])
    row['numero_telephone_maison'] = str(row['numero_telephone_maison'])
    row['adresse_postale'] = str(row['adresse_postale'])
    
    # Convert date to datetime
    if isinstance(row['date_naissance'], datetime.date):
        row['date_naissance'] = datetime.datetime.combine(row['date_naissance'], datetime.time.min)

    # Insert into MongoDB
    mongo_collection.insert_one(row)

print("Data migrated successfully from MySQL to MongoDB.")

# Close connections
cnx.close()
client.close()