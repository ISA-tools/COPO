__author__ = 'felix.shaw@tgac.ac.uk - 24/06/15'


from apps.web_copo.mongo.mongo_util import get_collection_ref
from allauth.socialaccount.models import SocialAccount

ORCID = get_collection_ref("OcidCollections")


class Orcid:

    def store_orcid_profile(self, profile_data, user):

        user_id = user.id
        social_account = SocialAccount.objects.get(user_id=user_id)
        profile_data = social_account.extra_data

        orcid_dict = {'user': user_id, 'orcid_profile': profile_data}

        ORCID.update({'user': user_id},
                     orcid_dict,
                     True)
