from django.test import TestCase
import pymongo

from project_copo.settings.settings import *


def get_collection_ref(collection_name):
    return pymongo.MongoClient(settings.MONGO_HOST, settings.MONGO_PORT)[settings.MONGO_DB][collection_name]


# Create your tests here.

class EnaTest(TestCase):
    def setUp(self):
        return get_collection_ref("Unit_Test_Collection")


    def setUp(self):
        self.db = get_collection_ref('test')


    def test_doc_published(self):
        # Set up a document to save
        doc = dict(text="test",
                      user_id=1)
        self.db.insert(doc)
        self.assertEqual(self.db.find_one(
            {'user_id':1})['text'], 'test')

    def tearDown(self):
        self.db.drop()

