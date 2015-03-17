__author__ = 'felixshaw'
from mongokit import Document, Connection
from bson import ObjectId

class MongoBase:

    connection = Connection(host="127.0.0.1", port=27017)
    db = 'MONGO_TEST_1'


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