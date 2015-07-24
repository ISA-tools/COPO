from django.test import TestCase
import pymongo

from settings.settings import *
from copo_id import get_uid


def get_collection_ref(collection_name):
    return pymongo.MongoClient(settings.MONGO_HOST, settings.MONGO_PORT)[settings.MONGO_DB][collection_name]


# Create your tests here.

class BasicTests(TestCase):
    def setUp(self):
        return get_collection_ref("Unit_Test_Collection")

    def test_doc_published(self):
        self.db = self.setUp()
        # Set up a document to save
        doc = dict(text="test",
                      user_id=1)
        self.db.insert(doc)
        self.assertEqual(self.db.find_one(
            {'user_id':1})['text'], 'test')

    def tearDown(self):
        self.db.drop()


class IdTest(TestCase):
    def setUp(self):
        pass

    def test_ids(self):
        id = get_uid()
        self.assertRegexpMatches(id, '[A-Z0-9]+', 'valid id not produced')

    def tearDown(self):
        pass




