__author__ = 'felixshaw'

from datetime import datetime

import bson.objectid as o
from django_tools.middlewares import ThreadLocal
from django.core.urlresolvers import reverse

from requests.exceptions import ConnectionError
from bson.objectid import ObjectId

from copo_id import get_uid
from web_copo.vocab.status_vocab import STATUS_CODES
from mongo_util import get_collection_ref
from base_resource import Resource

Profiles = get_collection_ref("Profiles")
Collections = get_collection_ref("CollectionHeads")


class Profile(Resource):
    def GET(self, id):
        s = 'abc'
        doc = Profiles.find_one({"_id": o.ObjectId(id)})
        if not doc:
            pass
        return doc

    def GET_FOR_USER(self, user=None):
        if(user == None):
            user = ThreadLocal.get_current_user().id
        docs = Profiles.find({'user_id':user})
        if not docs:
            pass
        return docs

    def GET_ALL(self):
        docs = Profiles.find()
        if not docs:
            pass
        return docs

    def get_profile_from_collection_id(self, collection_id):
        doc = Profiles.find_one({'collections': ObjectId(collection_id)})
        if doc:
            return doc
        else:
            return None

    def PUT(self, abstract, title, user_id):
        import platform

        sa = abstract[:147]
        sa += '...'

        # make unique copo id
        try:
            uid = get_uid()
        except ConnectionError:
            if platform.system() == 'Linux':
                return False
            else:
                uid = '0000000000000'

        spec = {
            "copo_id": uid,
            "title": title,
            "abstract": abstract,
            "short_abstract": sa,
            "date_created": datetime.now(),
            "date_modified": datetime.now(),
            "user_id": user_id,
        }
        return Profiles.insert(spec)

    def add_collection_head(self, profile_id, collection_id):
        return Profiles.update(
            {
                "_id": o.ObjectId(profile_id)
            },
            {
                '$push': {"collections": collection_id}
            }
        )


Collection_Heads = get_collection_ref("CollectionHeads")


class Collection_Head(Resource):
    # method to create a skelton collection object
    def PUT(self, c_type, c_name):

        spec = {
            "type": c_type,
            "name": c_name,
            "is_clean": False,
        }
        return Collection_Heads.insert(spec)

    def GET(self, id):
        return Collection_Heads.find_one({"_id": o.ObjectId(id)})

    def add_collection_details(self, collection_head_id, details_id):
        Collection_Heads.update(
            {
                "_id": o.ObjectId(collection_head_id)
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
        issues = {}
        issue_desc = []
        issue_id = []
        issues_count = 0
        user_id = ThreadLocal.get_current_user().id

        # get all profiles for user
        prof = Profiles.find({"user_id": user_id})

        # iterate profiles and find collections which are dirty
        for p in prof:
            try:
                collections_ids = p['collections']
            except:
                issues_count += 1
                context = {}
                context["profile_name"] = p['title']
                context["link"] = reverse('copo:view_profile', args=[p["_id"]])
                issue_desc.append(STATUS_CODES['PROFILE_EMPTY'].format(**context))
                break
            # now get the corresponding collection_heads
            collections_heads = Collections.find({'_id': {'$in': collections_ids}}, {'is_clean': 1, 'collection_details': 1})
            for c in collections_heads:
                try:
                    if c['is_clean'] == 0:
                        profile = Profile().get_profile_from_collection_id(c["_id"])
                        issues_count += 1
                        context = {}
                        context["profile_name"] = p['title']
                        context["link"] = reverse('copo:view_profile', args=[profile["_id"]])

                        #now work out why the collection is dirty
                        if False:
                            pass
                        else:
                            issue_desc.append(STATUS_CODES['PROFILE_NOT_DEPOSITED'].format(**context))
                except:
                    pass
        issues['issue_id_list'] = issue_id
        issues['num_issues'] = issues_count
        issues['issue_description_list'] = issue_desc
        return issues