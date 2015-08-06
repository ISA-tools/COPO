__author__ = 'felix.shaw@tgac.ac.uk - 24/06/15'

import json

from allauth.socialaccount.models import SocialAccount
from dal.base_resource import Resource
from dal.mongo_util import get_collection_ref

ORCID = get_collection_ref("OcidCollections")


class Orcid(Resource):

    def store_orcid_profile(self, profile_data, user):

        user_id = user.id
        social_account = SocialAccount.objects.get(user_id=user_id)
        profile_data = social_account.extra_data
        profile_data = json.dumps(profile_data).replace('-', '_')

        orcid_dict = {'user': user_id, 'op': json.loads(profile_data)}

        ORCID.update({'user': user_id},
                     orcid_dict,
                     True)


    def get_orcid_profile(self, user):

        u_id = user.id
        orc = ORCID.find_one({'user': u_id})
        if(orc != None):
            return orc
        else:
            return ''
