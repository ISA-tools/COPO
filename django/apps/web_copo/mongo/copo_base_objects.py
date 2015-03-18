__author__ = 'felixshaw'

from apps.web_copo.mongo.resource import *
import bson.objectid as o
from apps.web_copo.mongo.mongo_util import *
from datetime import datetime

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

    def ADD_COLLECTION(self, profile_id, collection_id):
        Profiles.update(
            {
                "_id": o.ObjectId(profile_id)
            },
            {
                '$push': {"collections": collection_id}
            }
        )

Collections = get_collection_ref("Collections")
class Collection(Resource):

    #method to create a skelton collection object
    def PUT(self, request):
        c_type = request.POST['collection_type']
        c_name = request.POST['collection_name']
        spec = {
            "type": c_type,
            "name": c_name,
        }
        return Collections.insert(spec)

    def GET(self, id):
        return Collections.find_one({"_id": o.ObjectId(id)})

