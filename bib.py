import json
import os
from pymongo import MongoClient
from dotenv import load_dotenv
from bson import json_util
from datetime import datetime
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

def export_mongo_to_json(collection_name):
    load_dotenv()
    # MongoDB Configuration
    mongo_db = os.environ.get('MONGO_DB')
    mongo_host = os.environ.get('MONGO_HOST')
    mongo_port = int(os.environ.get('MONGO_PORT'))  # convert to int because port should be a number

    client = MongoClient(f'mongodb://{mongo_host}:{mongo_port}/')

    db = client[mongo_db]
    mongo_collection = db[collection_name]

    data = list(mongo_collection.find())
    with open(f'{collection_name}.json', 'w') as f:
        json.dump(data, f, default=json_util.default)

    return data

def send_post_request_entree(numero_immatriculation):
    # Connection string for a local MongoDB instance
    uri = "mongodb+srv://kfsaidani:saidani2003@cluster0.adfmw12.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
    current_date = datetime.now().date()
    current_time = datetime.now().time()

    # Combine date and time
    current_time = datetime.combine(current_date, current_time)
    # Create a new client and connect to the server
    client = MongoClient(uri, server_api=ServerApi('1'))

    # Access the database and collection
    database = client['parkingDB']
    collection = database['entree__sortie']

    # Create a new document
    document = {
        'numero_immatriculation': numero_immatriculation,
        'heure_entree': str(current_time)
    }

    # Insert the document
    collection.insert_one(document)
    print("Inserted document successfully.")

def send_post_request_sortie(numero_immatriculation):
    # Connection string for a local MongoDB instance
    uri = "mongodb+srv://kfsaidani:saidani2003@cluster0.adfmw12.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
    current_date = datetime.now().date()
    current_time = datetime.now().time()

    # Combine date and time
    current_time = datetime.combine(current_date, current_time)
    # Create a new client and connect to the server
    client = MongoClient(uri, server_api=ServerApi('1'))

    # Access the database and collection
    database = client['parkingDB']
    collection = database['entree__sortie']

    # Find a document where 'numero_immatriculation' matches and 'heure_sortie' is not present
    document = collection.find_one({
        'numero_immatriculation': numero_immatriculation,
        'heure_sortie': {'$exists': False}
    })

    if document:
        # If a matching document is found, update it to add 'heure_sortie'
        collection.update_one(
            {'_id': document['_id']},
            {'$set': {'heure_sortie': str(current_time)}}
        )
        print(f"Updated document with _id {document['_id']} to add 'heure_sortie'.")
    else:
        print("No matching document found.")


def get_entree_sortie():
    # Connection string for a local MongoDB instance
    uri = "mongodb+srv://kfsaidani:saidani2003@cluster0.adfmw12.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

    # Create a new client and connect to the server
    client = MongoClient(uri, server_api=ServerApi('1'))

    # Access the database and collection
    database = client['parkingDB']
    collection = database['entree__sortie']

    # Find all documents in the collection
    documents = collection.find()

    uri = "mongodb://localhost:27017/?retryWrites=true&w=majority"
    client = MongoClient(uri)
    db = client['parkingDB']
    collection = db['entree__sortie']

    collection.insert_many(documents)