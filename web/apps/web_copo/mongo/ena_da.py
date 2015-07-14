from pprint import pprint

__author__ = 'felix.shaw@tgac.ac.uk - 18/03/15'

from datetime import date

import bson.objectid as o
import uuid
import ast

from apps.web_copo.mongo.resource import *
from apps.web_copo.mongo.mongo_util import *
import apps.web_copo.uiconfigs.utils.data_formats as dfmts
import apps.web_copo.uiconfigs.utils.lookup as lkup

EnaCollections = get_collection_ref("EnaCollections")


class EnaCollection(Resource):
    def GET(self, id):
        doc = EnaCollections.find_one({"_id": o.ObjectId(id)})
        if not doc:
            pass
        return doc

    def add_ena_study(self, ena_collection_id, study_type_list):
        ena_d = dfmts.json_to_dict(lkup.SCHEMAS["ENA"]['PATHS_AND_URIS']['ISA_json']);

        # let's store the generated study id...
        st_ids = []

        doc = EnaCollections.find_one({"_id": o.ObjectId(ena_collection_id)},
                                      {"studies": {"$elemMatch": {"id": {"$exists": False}}}})
        if doc and 'studies' in doc:  # adding studies for the first time, basically because placeholder study exists
            st_id = uuid.uuid4().hex
            EnaCollections.update({"_id": o.ObjectId(ena_collection_id)},
                                  {"$set": {"studies.0.id": st_id,
                                            "studies.0.study_type": study_type_list[0]['study_type'],
                                            "studies.0.study_type_reference": study_type_list[0][
                                                'study_type_reference']}})
            st_ids.append(st_id)
            del study_type_list[0]

        for x in range(0, len(study_type_list)):
            st_id = uuid.uuid4().hex
            study_dict = ena_d['studies'][0]
            study_dict['id'] = st_id
            study_dict['study_type'] = study_type_list[x]['study_type']
            study_dict['study_type_reference'] = study_type_list[x]['study_type_reference']

            EnaCollections.update({"_id": o.ObjectId(ena_collection_id)},
                                  {"$push": {"studies": study_dict}})
            st_ids.append(st_id)
        return st_ids

    def get_studies_tree(self, ena_collection_id):
        studies = self.GET(ena_collection_id)['studies']
        ena_studies = []

        for study in studies:
            a = {
                "id": study['id'] + "_study",
                "text": study['study_type_reference'] + " /" + dfmts.lookup_study_type_label(
                    study['study_type']) + " /" + "0",  # will change this to reflect the number of samples
                "state": "closed",
                "children": [
                    {
                        "id": study['id'] + "_publications",
                        "text": "Publications",  # this will eventually take their value from label in UI config
                        "state": "closed",
                        "children": []
                    },
                    {
                        "id": study['id'] + "_contacts",
                        "text": "Contacts",
                        "state": "closed",
                        "children": []
                    },
                    {
                        "id": study['id'] + "_samples",
                        "text": "Samples",
                        "state": "closed",
                        "children": []
                    },
                    {
                        "id": study['id'] + "_studyDescription",
                        "text": "Study Description"
                    }
                ]
            }

            ena_studies.append(a)

        return ena_studies

    def get_ena_study(self, study_id, ena_collection_id):
        doc = EnaCollections.find_one({"_id": o.ObjectId(ena_collection_id),
                                       "studies.id": study_id},
                                      {"studies.id.$": 1})
        if not doc:
            doc = {}
        return doc

    def add_study_samples(self, ena_collection_id, study_type_list, auto_fields):
        schema = "ENA"
        ena_full_json = dfmts.json_to_object(lkup.SCHEMAS[schema]['PATHS_AND_URIS']['UI_TEMPLATE_json'])
        ena_d = ena_full_json.studies.study.studySamples.fields
        auto_fields = ast.literal_eval(auto_fields)

        sample_ref = uuid.uuid4().hex
        a = {'ref': sample_ref}

        for f in ena_d:
            key_split = f.id.split(".")
            a[key_split[len(key_split) - 1]] = ""  # accommodates fields not displayed on form
            if f.id in auto_fields.keys():
                a[key_split[len(key_split) - 1]] = auto_fields[f.id]

        ena_d = ena_full_json.studies.study.studySamples.sampleCollection.fields

        for f in ena_d:
            key_split = f.id.split(".")
            a[key_split[len(key_split) - 1]] = ""
            if f.id in auto_fields.keys():
                a[key_split[len(key_split) - 1]] = auto_fields[f.id]

        EnaCollections.update({"_id": o.ObjectId(ena_collection_id)},
                              {"$push": {"copoInternal.sampleTypes": a}})

        # now do the study<->sample assignment
        for val in study_type_list:
            a = {'sampleType_ref': sample_ref,
                 'studyType_ref': val,
                 'id': uuid.uuid4().hex,
                 'deleted': '0'
                 }
            EnaCollections.update({"_id": o.ObjectId(ena_collection_id)},
                                  {"$push": {"copoInternal.studySamples": a}})

    def remove_study_sample(self, ena_collection_id, study_samples_id):
        EnaCollections.update({"_id": ObjectId(ena_collection_id), "copoInternal.studySamples._id": study_samples_id},
                              {'$set': {"copoInternal.studySamples.$.deleted": "1"}})

    def add_study(self, values, attributes):
        spec_attr = []
        for att_group in attributes:
            tmp = {
                "tag": att_group[0],
                "value": att_group[1],
                "unit": att_group[2],
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
                "tag": att_group[0],
                "value": att_group[1],
                "unit": att_group[2],
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
        # create new sample and add to study

        spec_attr = []
        for att_group in attributes:
            tmp = {
                "id": o.ObjectId(),
                "tag": att_group[0],
                "value": att_group[1],
                "unit": att_group[2],
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
                "tag": att_group[0],
                "value": att_group[1],
                "unit": att_group[2],
            }
            spec_attr.append(tmp)
        x = sample['Source_Name']
        EnaCollections.update(
            {"_id": ObjectId(study_id), "samples._id": ObjectId(sample_id)},
            {'$set': {"samples.$.Source_Name": sample['Source_Name'], "samples.$.Characteristics": spec_attr,
                      "samples.$.Term_Source_REF": "TODO:ONTOLOGY", "samples.$.Protocol_REF": "TODO:PROTOCOL_STRING",
                      "samples.$.Sample_Name": sample['Anonymized_Name'],
                      "samples.$.Individual_Name": sample['Individual_Name'],
                      "samples.$.Description": sample['Description'], "samples.$.Taxon_ID": sample['Taxon_ID'],
                      "samples.$.Scientific_Name": sample['Scientific_Name'],
                      "samples.$.Common_Name": sample['Common_Name'],
                      "samples.$.Anonymized_Name": sample["Anonymized_Name"]}}
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
            "last_updated": str(date.today()),
        }
        EnaCollections.update(
            {"_id": o.ObjectId(study_id)},
            {'$push':
                 {"experiments": spec}
             }
        )
        return str(exp_id)

    def update_experiment_in_study(self, per_panel, common, study_id):
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
            "last_updated": str(date.today()),
        }
        EnaCollections.update(
            {"_id": ObjectId(study_id), "experiments._id": ObjectId(experiment_id)},
            {
                '$set': {
                    "experiments.$.Parameter_Value[sequencing instrument]": common['platform'] + " " + common['model'],
                    "experiments.$.Parameter_Value[library_source]": common['lib_source'],
                    "experiments.$.Parameter_Value[library_selection]": common['lib_selection'],
                    "experiments.$.Parameter_Value[lib_strategy]": common['lib_strategy'],
                    "experiments.$.Library_Name": per_panel['lib_name'],
                    "experiments.$.panel_ordering": int(per_panel['panel_ordering']),
                    "experiments.$.panel_id": per_panel['panel_id'],
                    "experiments.$.data_modal_id": per_panel['data_modal_id'],
                    "experiments.$.copo_exp_name": common['copo_exp_name'], "experiments.$.insert_size": insert_size,
                    "experiments.$.study_id": ObjectId(common['study']),
                    "experiments.$.study_id": ObjectId(common['study']),
                    "experiments.$.sample_id": ObjectId(per_panel['sample_id']),
                    "experiments.$.Sample_Name": per_panel['sample_name'],
                    "experiments.$.file_type": per_panel['file_type']}}
        )
        return experiment_id

    def add_file_to_study(self, study_id, experiment_id, chunked_upload_id, hash):
        _id = ObjectId()
        spec = {
            "_id": str(_id),
            "experiment_id": str(experiment_id),
            "chunked_upload_id": chunked_upload_id,
            "hash": hash,
        }
        EnaCollections.update(
            {"_id": ObjectId(study_id)},
            {"$push": {"files": spec}}
        )

    def get_experiment_by_id(self, study_id):
        return EnaCollections.find_one({"_id": ObjectId(study_id)}, {"experiments": 1, "_id": 0})

    def get_experiments_by_modal_id(self, modal_id):
        return EnaCollections.find({"experiments.data_modal_id": modal_id}, {"experiments.$": 1})

    def get_distict_experiment_ids_in_study_(self, study_id):
        return EnaCollections.find({"_id": ObjectId(study_id)}).distinct("experiments.data_modal_id")

    def get_chunked_upload_id_from_file_id(self, file_id):
        return EnaCollections.find({"experiments.files": ObjectId(file_id)}, {"experiments.files.$": 1})

    def get_files_by_experiment_id(self, experiment_id):
        return EnaCollections.aggregate([
            {"$match": {"files.experiment_id": str(experiment_id)}},
            {"$unwind": "$files"},
            {"$match": {"files.experiment_id": str(experiment_id)}},
            {"$project": {"files": 1}}
        ])

    def remove_file_from_experiment(self, file_id):
        return EnaCollections.update({"files.chunked_upload_id": int(file_id)},
                                     {"$pull": {"files": {"chunked_upload_id": int(file_id)
                                                          }}})
