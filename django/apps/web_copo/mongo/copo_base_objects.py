__author__ = 'felixshaw'

import pymongo
from resource import *
from mongo_util import get_collection_ref
from datetime import datetime

Profiles = get_collection_ref("Profiles")
class Profile(Resource):

    def GET(self, request, id):
        spec = {"_id": id}
        doc = Profiles.find_one(spec)
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