__author__ = 'felixshaw'

from datetime import datetime

import bson.objectid as o

from apps.web_copo.mongo.resource import *
from apps.web_copo.mongo.mongo_util import *


Profiles = get_collection_ref("Profiles")
class Profile(Resource):

    def GET(self, id):

        doc = Profiles.find_one({"_id": o.ObjectId(id)})
        if not doc:
            pass
        return doc

    def GET_ALL(self):
        docs = Profiles.find()
        if not docs:
            pass
        return docs

    def PUT(self, request):
        a = request.POST['study_abstract']
        sa = a[:147]
        sa += '...'

        spec = {
            "title": request.POST['study_title'],
            "abstract": a,
            "short_abstract": sa,
            "date_created": datetime.now(),
            "date_modified": datetime.now(),
            "user_id": request.user.id
        }
        Profiles.insert(spec)

    def add_collection_head(self, profile_id, collection_id):
        Profiles.update(
            {
                "_id": o.ObjectId(profile_id)
            },
            {
                '$push': {"collections": collection_id}
            }
        )


Collection_Heads = get_collection_ref("Collection_Heads")
class Collection_Head(Resource):

    #method to create a skelton collection object
    def PUT(self, request):
        c_type = request.POST['collection_type']
        c_name = request.POST['collection_name']
        spec = {
            "type": c_type,
            "name": c_name,
        }
        return Collection_Heads.insert(spec)

    def GET(self, id):
        return Collection_Heads.find_one({"_id": o.ObjectId(id)})

    def add_collection_details(self, collection_id, details_id):
        Collection_Heads.update(
            {
                "_id": o.ObjectId(collection_id)
            },
            {
                '$set': {"collection_details": details_id}
            }
        )

    def collection_details_id_from_head(self, head_id):
        collection = Collection_Heads.find_one({"_id":o.ObjectId(head_id)})
        return 0