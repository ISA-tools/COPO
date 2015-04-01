__author__ = 'felix.shaw@tgac.ac.uk - 18/03/15'

from apps.web_copo.mongo.resource import *
import bson.objectid as o
import bson.objectid
from apps.web_copo.mongo.mongo_util import *
import uuid
EnaCollections = get_collection_ref("EnaCollections")

class EnaCollection(Resource):

    def GET(self, id):
        doc = EnaCollections.find_one({"_id": o.ObjectId(id)})
        if not doc:
            pass
        return doc

    def get_sample(self, sample_id):
        doc = EnaCollections.find_one({"samples._id": o.ObjectId(sample_id)}, {"samples.$": 1})
        return doc['samples'][0]

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
            "Study_Title": values['study_title'],
            "Study_Abstract": values['study_abstract'],
            "Center_Name": values['center_name'],
            "Study_Description": values['study_description'],
            "Center_Project_Name": values['center_project_name'],
            "Study_Attributes": spec_attr,
        }
        return EnaCollections.insert(spec)

    def update_study(self, ena_study_id, values, attributes):
        spec_attr = []
        for att_group in attributes:
            tmp = {
                "tag":att_group[0],
                "value":att_group[1],
                "unit":att_group[2],
            }
            spec_attr.append(tmp)
        spec = {
            "Study_Title": values['study_title'],
            "Study_Abstract": values['study_abstract'],
            "Center_Name": values['center_name'],
            "Study_Description": values['study_description'],
            "Center_Project_Name": values['center_project_name'],
            "Study_Attributes": spec_attr,
        }
        return EnaCollections.update(
            {
                "_id": o.ObjectId(ena_study_id)
            },
            spec
        )

    def add_sample_to_study(self, sample, attributes, study_id):
        #create new sample and add to study

        spec_attr = []
        for att_group in attributes:
            tmp = {
                "id": o.ObjectId(),
                "tag":att_group[0],
                "value":att_group[1],
                "unit":att_group[2],
            }
            spec_attr.append(tmp)
        spec = {
            "_id": o.ObjectId(),
            "Source_Name": sample['Source_Name'],
            "Characteristics": spec_attr,
            "Term_Source_REF": "TODO:ONTOTLOGY_ID",
            "Term_Accession_Number": sample['Taxon_ID'],
            "Protocol_REF": "TODO:PROTOCOL_STRING",
            "Sample_Name": sample['Anonymized_Name'],
            "Individual_Name": sample['Individual_Name'],
            "Description": sample['Description'],
            "Taxon_ID": sample['Taxon_ID'],
            "Scientific_Name": sample['Scientific_Name'],
            "Common_Name": sample['Common_Name'],
            "Anonymized_Name": sample["Anonymized_Name"],

        }

        EnaCollections.update(
            {

                "_id": o.ObjectId(study_id)
            },
            {
                '$push': {"samples": spec}
            }
        )

    def update_sample_in_study(self, sample, attributes, study_id, sample_id):
        spec_attr = []
        for att_group in attributes:
            tmp = {
                "tag":att_group[0],
                "value":att_group[1],
                "unit":att_group[2],
            }
            spec_attr.append(tmp)
        x = sample['Source_Name']
        EnaCollections.update(
            {"_id": ObjectId(study_id), "samples._id": ObjectId(sample_id)},
            { '$set': { "samples.$.Source_Name": sample['Source_Name'], "samples.$.Characteristics": spec_attr, "samples.$.Term_Source_REF": "TODO:ONTOLOGY","samples.$.Protocol_REF": "TODO:PROTOCOL_STRING","samples.$.Sample_Name": sample['Anonymized_Name'],"samples.$.Individual_Name": sample['Individual_Name'],"samples.$.Description": sample['Description'],"samples.$.Taxon_ID": sample['Taxon_ID'],"samples.$.Scientific_Name": sample['Scientific_Name'],"samples.$.Common_Name": sample['Common_Name'],"samples.$.Anonymized_Name": sample["Anonymized_Name"]} }
        )
        '''
        EnaCollections.update(
            {"_id": ObjectId(study_id), "samples._id": ObjectId(sample_id)},
            {'$set:': {"samples.$.Source_Name": x,"samples.$.Characteristics": spec_attr,"samples.$.Term_Source_REF": "TODO:ONTOLOGY","samples.$.Protocol_REF": "TODO:PROTOCOL_STRING","samples.$.Sample_Name": sample['Anonymized_Name'],"samples.$.Individual_Name": sample['Individual_Name'],"samples.$.Description": sample['Description'],"samples.$.Taxon_ID": sample['Taxon_ID'],"samples.$.Scientific_Name": sample['Scientific_Name'],"samples.$.Common_Name": sample['Common_Name'],"samples.$.Anonymized_Name": sample["Anonymized_Name"]}}
        )

        EnaCollections.update(
            {"_id": ObjectId(study_id), "samples._id": ObjectId(sample_id)},
                { '$set': { "samples.$.Common_Name": "44444", "samples.$.Description": "tw@" } }
        )
        '''