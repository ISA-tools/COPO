from django.test import TestCase
import pymongo

from master_settings import *
from copo_id import get_uid


def get_collection_ref(collection_name):
    return pymongo.MongoClient(settings.MONGO_HOST, settings.MONGO_PORT)[settings.MONGO_DB][collection_name]


# Create your copo_tests here.

class ViewTests(TestCase):

    def testview(self):
        pass


class IdTest(TestCase):

    def test_ids(self):
        id = get_uid()
        self.assertRegexpMatches(id, '[A-Z0-9]+', 'valid id not produced')




