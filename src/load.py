from pymongo import MongoClient


def load_evolution_to_mongo(evolution, mongo_uri, db_name, collection_name):
    client = MongoClient(mongo_uri)
    db = client[db_name]
    collection = db[collection_name]

    collection.delete_many({})

    collection.insert_many(evolution)

    client.close()
