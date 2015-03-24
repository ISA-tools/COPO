__author__ = 'felix.shaw@tgac.ac.uk - 18/03/15'

from apps.web_copo.mongo.resource import *
import bson.objectid as o
from apps.web_copo.mongo.mongo_util import *
import uuid
EnaCollections = get_collection_ref("EnaCollections")

class EnaCollection(Resource):

    def GET(self, id):
        doc = EnaCollections.find_one({"_id": o.ObjectId(id)})
        if not doc:
            pass
        return doc

    def add_study(self, values, attributes):
        spec_attr = []
        for att_group in attributes:
            tmp = {
                "tag":att_group[0],
                "value":att_group[1],
                "unit":att_group[2],
            }
            spec_attr.append(tmp)
        spec = {
            "Study_Identifier": str(uuid.uuid1()),
            "Study_Title": values['STUDY_TITLE'],
            "Study_Abstract": values['STUDY_ABSTRACT'],
            "Center_Name": values['CENTER_NAME'],
            "Study_Description": values['STUDY_DESCRIPTION'],
            "Center_Project_Name": values['CENTER_PROJECT_NAME'],
            "Study_Attributes": spec_attr,
        }
        return EnaCollections.insert(spec)

    def add_sample_to_study(self, sample, attributes, study_id):
        #create new sample and add to study

        spec_attr = []
        for att_group in attributes:
            tmp = {
                "tag":att_group[0],
                "value":att_group[1],
                "unit":att_group[2],
            }
            spec_attr.append(tmp)
        spec = {
            "Source Name": sample['TITLE'],
            "Characteristics[organism]": spec_attr,
            "Term Source REF": "TODO:ONTOTLOGY_ID",
            "Term Accession Number": sample['TAXON_ID'],
            "Protocol REF": "TODO:PROTOCOL_STRING",
            "Sample Name": sample['ANONYMIZED_NAME'],
        }

        EnaCollections.update(
            {
                "_id": o.ObjectId(study_id)
            },
            {
                '$push': {"samples": spec}
            }
        )