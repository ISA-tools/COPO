__author__ = 'felixshaw'
from mongokit import Connection
from django.conf import *
from bson import ObjectId

connection = Connection(host=settings.MONGO_HOST, port=settings.MONGO_PORT)
db = settings.MONGO_DB


def to_mongo_id(id):
    return ObjectId(id)

# django templates take a list or dictionary object as their context, so mongodb cursor objects
# need to be converted before being used in templates
def to_django_context(cursor):
    records = []
    for r in cursor:
        records.append(r.to_json_type())
    return records