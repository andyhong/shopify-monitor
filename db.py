from pymongo import MongoClient
from pymongo.errors import OperationFailure

print("Initializing database...")

client = MongoClient("mongodb+srv://andy:hong@cluster0-nxetg.mongodb.net/shopify?retryWrites=true&w=majority")

try:
    client.admin.command("ismaster")
    db = client["shopify"]
    print("Connected to DB!")
except OperationFailure:
    print("Connection to DB failed.")

def init_db(db):

    # Drops all existing collections.
    
    print("Deleting existing collections...")
    for col in db.list_collection_names():
        db[col].drop()