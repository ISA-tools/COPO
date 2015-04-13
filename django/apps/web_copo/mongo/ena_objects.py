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
            {"_id": o.ObjectId(study_id)},
            {'$push':
                 {"samples": spec}
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


    def get_sample(self, sample_id):
        doc = EnaCollections.find_one({"samples._id": o.ObjectId(sample_id)}, {"samples.$": 1})
        return doc['samples'][0]


    def get_samples_in_study(self, study_id):
        doc = EnaCollections.find({"_id": ObjectId(study_id)}, {"samples": 1})
        return doc


    def add_experiment_to_study(self, per_panel, common, study_id):
        exp_id = ObjectId()
        try:
            insert_size = int(common['insert_size'])
        except:
            insert_size = 0
        spec = {
            "_id": exp_id,
            "Parameter_Value[sequencing instrument]": common['platform'] + " " + common['model'],
            "Parameter_Value[library_source]": common['lib_source'],
            "Parameter_Value[library_selection]": common['lib_selection'],
            "Parameter_Value[lib_strategy]": common['lib_strategy'],
            "Library_Name": per_panel['lib_name'],
            "panel_ordering": int(per_panel['panel_ordering']),
            "panel_id": per_panel['panel_id'],
            "data_modal_id": per_panel['data_modal_id'],
            "copo_exp_name": common['copo_exp_name'],
            "insert_size": insert_size,
            "study_id": ObjectId(common['study']),
            "sample_id": ObjectId(per_panel['sample_id']),
            "Sample_Name": per_panel['sample_name'],
            "file_type": per_panel['file_type'],
        }
        EnaCollections.update(
            {"_id": o.ObjectId(study_id)},
            {'$push':
                 {"experiments": spec}
            }
        )
        return str(exp_id)


    def update_experiment_in_study(self, common, per_panel, study_id):
        experiment_id = per_panel['experiment_id']
        try:
            insert_size = int(common['insert_size'])
        except:
            insert_size = 0
        spec = {
            "platform": common['platform'],
            "instrument": common['model'],
            "lib_source": common['lib_source'],
            "lib_selection": common['lib_selection'],
            "lib_strategy": common['lib_strategy'],
            "panel_ordering": int(per_panel['panel_ordering']),
            "panel_id": per_panel['panel_id'],
            "data_modal_id": per_panel['data_modal_id'],
            "copo_exp_name": common['copo_exp_name'],
            "insert_size": insert_size,
            "study_id": ObjectId(common['study']),
            "sample_id": ObjectId(per_panel['sample_id']),
            "lib_name": per_panel['lib_name'],
            "file_type": per_panel['file_type'],
        }
        EnaCollections.update(
            {"_id": ObjectId(study_id), "experiments._id": ObjectId(experiment_id)},
            { '$set': { "experiments.$.Parameter_Value[sequencing instrument]": common['platform'] + " " + common['model'], "experiments.$.Parameter_Value[library_source]": common['lib_source'], "experiments.$.Parameter_Value[library_selection]": common['lib_selection'],"experiments.$.Parameter_Value[lib_strategy]": common['lib_strategy'],"experiments.$.Library_Name": per_panel['lib_name'],"experiments.$.panel_ordering": int(per_panel['panel_ordering']),"experiments.$.panel_id": per_panel['panel_id'],"experiments.$.data_modal_id": per_panel['data_modal_id'],"experiments.$.copo_exp_name": common['copo_exp_name'],"experiments.$.insert_size": insert_size,"experiments.$.study_id": ObjectId(common['study']),"experiments.$.study_id": ObjectId(common['study']),"experiments.$.sample_id": ObjectId(per_panel['sample_id']),"experiments.$.Sample_Name": per_panel['sample_name'],"experiments.$.file_type": per_panel['file_type']} }
        )
        return experiment_id


    def add_file_to_experiment(self, experiment_id, chunked_upload_id, hash):
        _id = ObjectId()
        spec = {
            "_id": str(_id),
            "chunked_upload_id": chunked_upload_id,
            "hash": hash,
        }
        EnaCollections.update(
            {"experiments._id": ObjectId(experiment_id)},
            {"$push":{"experiments.$.files":spec}}
        )


