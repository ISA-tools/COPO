__author__ = 'felixshaw'
import pymongo
from django.conf import *
from bson import ObjectId

#connection = Connection(host=settings.MONGO_HOST, port=settings.MONGO_PORT)
#db = settings.MONGO_DB

def get_collection_ref(collection_name):
    return pymongo.Connection(settings.MONGO_HOST, settings.MONGO_PORT)[settings.MONGO_DB][collection_name]

def to_mongo_id(id):
    return ObjectId(id)

# django templates take a list or dictionary object as their context, so mongodb cursor objects
# need to be converted before being used in templates
def to_django_context(cursor):
    records = []
    for r in cursor:
        records.append(r.to_json_type())
    return records



