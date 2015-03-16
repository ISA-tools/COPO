__author__ = 'felixshaw'

from mongokit import Document
from bson import ObjectId

class MongoBase(Document):
    # ObjectId objects are used in mongodb queries where the default id object is of this type
    def to_mongo_id(id):
        return ObjectId(id)

    # django templates take a list or dictionary object as their context, so mongodb cursor objects
    # need to be converted before being used in templates
    def to_django_context(cursor):
        records = []
        for r in cursor:
            records.append(r.to_json_type())
        return records