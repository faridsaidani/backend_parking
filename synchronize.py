from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from bib import export_mongo_to_json, get_user_id
import sys
from datetime import datetime

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

if __name__ == "__main__":
    if len(sys.argv) > 1:
        collection = sys.argv[1]
    else:
        print("No command-line argument provided.")
        exit()
    uri = "mongodb+srv://kfsaidani:saidani2003@cluster0.adfmw12.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
    migrate_data(collection, uri)