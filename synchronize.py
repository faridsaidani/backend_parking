from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from bib import export_mongo_to_json
import sys

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