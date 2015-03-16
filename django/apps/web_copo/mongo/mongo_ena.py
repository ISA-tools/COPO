__author__ = 'felixshaw'

from mongokit import Connection
from django.conf import settings
from mongo_base import MongoBase


connection = Connection(host=settings.MONGO_HOST, port=settings.MONGO_PORT)
db = settings.MONGO_DB



@connection.register
class EnaSub(MongoBase):
    # allows additional fields to be added to the document on the fly
    use_schemaless = True
    # shortcut to the collection these documents are store in
    __collection__ = 'enasubs'
    # shortcut to the database name
    __database__ = db
    # allows use of dot.notation instead of dict['notation'] (doesn't seem to work for schemaless fields)
    use_dot_notation = True
    use_autorefs = True
    structure = {
        'title': basestring,
        'abstract': basestring,
        'short_abstract': [basestring],



    }
    required_fields = ['firstname', 'lastname']
    default_values = { }
