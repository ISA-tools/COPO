__author__ = 'felixshaw'
import pymongo
from bson import ObjectId

from settings import master_settings


def get_collection_ref(collection_name):
    return pymongo.MongoClient(master_settings.MONGO_HOST, master_settings.MONGO_PORT)[master_settings.MONGO_DB][collection_name]

def to_mongo_id(id):
    return ObjectId(id)

# web templates take a list or dictionary object as their context, so mongodb cursor objects
# need to be converted before being used in templates
def to_django_context(cursor):
    records = []
    for r in cursor:
        records.append(r.to_json_type())
    return records

def cursor_to_list(cursor):
    records = []
    for r in cursor:
        records.append(r)
    return records


