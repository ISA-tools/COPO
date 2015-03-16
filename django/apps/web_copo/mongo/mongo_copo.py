__author__ = 'felixshaw'

from mongokit import Connection, Document

from datetime import datetime
from mongo_util import *
import uuid



@connection.register
class Profile(Document):
    # allows additional fields to be added to the document on the fly
    use_schemaless = True
    # shortcut to the collection these documents are store in
    __collection__ = 'profiles'
    # shortcut to the database name
    __database__ = db
    # allows use of dot.notation instead of dict['notation'] (doesn't seem to work for schemaless fields)
    use_dot_notation = True

    structure = {
        'title':basestring,
        'abstract':basestring,
        'short_abstract':basestring,
        'date_created':datetime,
        'date_modified':datetime,
        'user':long,

        'collections':{
            'id':basestring,
            'name':basestring,
            'type':basestring,
            }

    }
    indexes = [
        {
            'fields':'collections.id',
            'unique':True,
        }
    ]
