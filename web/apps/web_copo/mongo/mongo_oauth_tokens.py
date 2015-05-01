__author__ = 'felix.shaw@tgac.ac.uk - 30/04/15'


from apps.web_copo.mongo.resource import *
import bson.objectid as o
from apps.web_copo.mongo.mongo_util import *
from datetime import datetime
from django_tools.middlewares import ThreadLocal

FigshareTokens = get_collection_ref("Figshare_tokens")

class Figshare_token(Resource):

    def token_exists(self):
        user = ThreadLocal.get_current_user()
        return(FigshareTokens.find({'user_id': user.id}).limit(1).count() > 0 )

    def delete_old_token(self):
        user = ThreadLocal.get_current_user()
        FigshareTokens.delete_many({'user_id': user.id})

    def get_token_from_db(self):
        user = ThreadLocal.get_current_user()
        return FigshareTokens.find_one({'user_id': user.id})

    def add_token(self, owner_key=None, owner_secret=None):
        user = ThreadLocal.get_current_user()
        FigshareTokens.insert({'user_id': user.id, 'owner_key': owner_key, 'owner_secret': owner_secret})
