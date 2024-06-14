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

def get_user_id(numero_immatriculation):
    # Connection string for a local MongoDB instance
    uri = "mongodb://localhost:27017/"

    # Create a new client and connect to the server
    client = MongoClient(uri, server_api=ServerApi('1'))

    # Access the database and collection
    database = client['parkingDB']
    vehicules = database['vehicule']
    print(numero_immatriculation)
    # Query the collection for a document with the specified numero_immatriculation
    vehicule = vehicules.find_one({'numero_immatriculation': numero_immatriculation})
    print(vehicule)
    # Return the user id if a matching document was found, otherwise return None
    return vehicule['propietaire'] if vehicule else None

def process_all_vehicles():
    # Connection string for a local MongoDB instance
    uri = "mongodb://localhost:27017/"

    # Create a new client and connect to the server
    client = MongoClient(uri, server_api=ServerApi('1'))

    # Access the database and collection
    database = client['parkingDB']
    vehicules = database['vehicule']

    # Retrieve all documents from the vehicule collection
    all_vehicles = vehicules.find()

    # For each document, call send_post_request_entree and send_post_request_sortie
    for vehicle in all_vehicles:
        numero_immatriculation = vehicle['numero_immatriculation']
        send_post_request_entree(numero_immatriculation)
        send_post_request_sortie(numero_immatriculation)


def sync_factures():
    uri = "mongodb://localhost:27017/"
    client = MongoClient(uri, server_api=ServerApi('1'))
    database = client['parkingDB']
    entree_sortie = database['entree__sortie']
    factures = database['facture']
    documents = entree_sortie.find()
    for document in documents:
        if isinstance(document['heure_entree'], datetime) and isinstance(document['heure_sortie'], datetime):
            heure_entree = document['heure_entree']
            heure_sortie = document['heure_sortie']
        else:
            heure_entree = datetime.strptime(document['heure_entree'], "%Y-%m-%d %H:%M:%S.%f")
            heure_sortie = datetime.strptime(document['heure_sortie'], "%Y-%m-%d %H:%M:%S.%f")
        time_difference = (heure_sortie - heure_entree).total_seconds() / 60
        if time_difference < 30:
            tarif = 1.8
        elif 30 <= time_difference < 60:
            tarif = 1.6
        else:
            tarif = 1.2
        total_cost = time_difference * tarif
        uid = get_user_id(document['numero_immatriculation'])
        facture = {
            'id_utilisateur' : uid,
            'numero_immatriculation': document['numero_immatriculation'],
            'heure_entree': document['heure_entree'],
            'heure_sortie': document['heure_sortie'],
            'tarif': tarif,
            'total_cost': total_cost,
            'regle' : False
        }
        factures.insert_one(facture)

def migrate_data(collection_name, uri):
    data = export_mongo_to_json(collection_name)
    print(data)

    # Create a new client and connect to the server
    client = MongoClient(uri, server_api=ServerApi('1'))

    # Send a ping to confirm a successful connection
    try:
        client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
        # Print the available databases
        print(client.list_database_names())
        database = client['parkingDB']
        # print the collections in the database
        print(database.list_collection_names())
        if collection_name in database.list_collection_names():
            print(f"The collection {collection_name} already exists.")
        else:
            database.create_collection(collection_name)
        collection = database[collection_name]
        # print the documents in the collection

        for record in data:
            print(record)
            try: 
                existing_document = collection.find_one({'_id': record['_id']})
                if existing_document:
                    print(f"A document with _id {record['_id']} already exists.")
                else:
                    collection.insert_one(record)
            except Exception as e:
                print(e)
        print("Data migrated successfully from MongoDB to MongoDB.")
    except Exception as e:
        print(e)