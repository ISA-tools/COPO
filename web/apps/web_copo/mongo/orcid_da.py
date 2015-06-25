__author__ = 'felix.shaw@tgac.ac.uk - 24/06/15'


from apps.web_copo.mongo.mongo_util import *

ORCID = get_collection_ref("OcidCollections")


class Orcid:

    def store_orcid_profile(self, profile_data, user):

        user_id = user.id
        #ORCID.insert()
        print(profile_data)
        print(user_id)