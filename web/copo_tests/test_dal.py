from django.test import TestCase
from bson.objectid import ObjectId

import dal.copo_base_da as base
import dal.ena_da as ena_da
from web_copo.uiconfigs.utils.data_utils import get_ena_db_template


class DalTests(TestCase):

    def setUp(self):
        from dal.mongo_util import get_collection_ref
        # empty all collections in test_db
        get_collection_ref('Profiles').drop()
        get_collection_ref('FigshareCollections').drop()
        get_collection_ref('OrcidCollections').drop()
        get_collection_ref('EnaCollections').drop()
        get_collection_ref('CollectionHeads').drop()


    # PROFILE TESTS ===================================================

    def test_profile_put(self):

        profile_id = base.Profile().PUT('test abstract', 'test title', 21)
        self.assertIsInstance(profile_id, ObjectId, 'Profile not created')


    def test_profile_get(self):

        profile_id = base.Profile().PUT('test abstract', 'test title', 21)
        profile = base.Profile().GET(profile_id)
        self.assertEqual(profile['abstract'], 'test abstract', 'Error Retrieving profile')
        self.assertEqual(profile['title'], 'test title', 'Error Retrieving profile')
        self.assertEqual(profile['user_id'], 21, 'Error Retrieving profile')


    def test_get_profiles_for_user(self):

        base.Profile().PUT('test abstract1', 'test title', 21)
        base.Profile().PUT('test abstract2', 'test title', 21)
        base.Profile().PUT('test abstract3', 'test title', 21)
        profiles = base.Profile().GET_FOR_USER(21)
        self.assertEqual(profiles.count(), 3, 'Error in number of profiles for user')


    def test_get_all(self):

        base.Profile().PUT('test abstract1', 'test title', 21)
        base.Profile().PUT('test abstract2', 'test title', 21)
        base.Profile().PUT('test abstract3', 'test title', 21)
        profiles = base.Profile().GET_ALL()
        self.assertEqual(profiles.count(), 3, 'Error in get all profiles')



    # COLLECTION TESTS ===================================================

    def test_collection_put(self):

        collection_id = base.Collection_Head().PUT('type', 'name')
        self.assertIsInstance(collection_id, ObjectId, 'Error creating collection head')


    def test_collection_get(self):

        collection_id = base.Collection_Head().PUT('type', 'name')
        collection = base.Collection_Head().GET(collection_id)
        self.assertEqual(collection['type'], 'type', 'Error retrieving collection')
        self.assertEqual(collection['name'], 'name', 'Error retrieving collection')


    def test_add_collection_to_profile(self):

        p = base.Profile()
        profile_id = p.PUT('test abstract1', 'test title', 21)
        collection_id = base.Collection_Head().PUT('type', 'name')
        result = p.add_collection_head(profile_id, collection_id)
        self.assertEqual(result['updatedExisting'], True, 'Error adding collection to profile')
        self.assertEqual(result['ok'], 1, 'Error adding collection to profile')


    def test_get_profile_from_collection_id(self):

        p = base.Profile()
        profile_id = p.PUT('test abstract1', 'test title', 21)
        collection_id = base.Collection_Head().PUT('type', 'name')
        p.add_collection_head(profile_id, collection_id)
        p_id = p.get_profile_from_collection_id(collection_id)
        self.assertEqual(profile_id, p_id['_id'], 'Error getting profile from collection id')


    def test_add_collection_details(self):

        c = base.Collection_Head()
        f = ena_da.EnaCollection()
        ena_tmpl = get_ena_db_template()
        ena_collection_id = base.get_collection_ref("EnaCollections").insert(ena_tmpl)





    def tearDown(self):

        from dal.mongo_util import get_collection_ref
        # empty all collections in test_db
        get_collection_ref('Profiles').drop()
        get_collection_ref('FigshareCollections').drop()
        get_collection_ref('OrcidCollections').drop()
        get_collection_ref('EnaCollections').drop()
        get_collection_ref('CollectionHeads').drop()


