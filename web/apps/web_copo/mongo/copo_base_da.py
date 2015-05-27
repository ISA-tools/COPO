__author__ = 'felixshaw'

from datetime import datetime

import bson.objectid as o
from django_tools.middlewares import ThreadLocal

from apps.web_copo.mongo.resource import *
from apps.web_copo.mongo.mongo_util import *


Profiles = get_collection_ref("Profiles")
Collections = get_collection_ref("Collection_Heads")


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
    # method to create a skelton collection object
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
        collection = Collection_Heads.find_one({"_id": o.ObjectId(head_id)})
        return 0


class Profile_Status_Info(Resource):
    def get_profiles_status(self):
        # this method examines all the profiles owned by the current user and returns
        # the number of profiles which have been marked as dirty

        issues_count = 0
        user_id = ThreadLocal.get_current_user().id

        # get all profiles for user
        prof = Profiles.find({"user_id": user_id})

        # iterate profiles and find collections which are dirty
        for p in prof:
            collections_ids = p['collections']
            # now get the corresponding collection_heads
            collections_heads = Collections.find({'_id': {'$in': collections_ids}}, {'is_clean': 1, '_id': 0})
            for c in collections_heads:
                try:
                    if c['is_clean'] == 0:
                        issues_count += 1
                except:
                    pass

        return issues_count