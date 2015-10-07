__author__ = 'felix.shaw@tgac.ac.uk - 18/03/15'

from datetime import date
import string
import uuid
import ast

import dal.mongo_util as mutil




#from dal.resource import *
#from web_copo.mongo.mongo_util import *
import random
import web.apps.web_copo.copo_maps.utils.data_utils as d_utils

from dal.mongo_util import get_collection_ref
from dal.base_resource import Resource
from dal import ObjectId

EnaCollections = get_collection_ref("EnaCollections")


class EnaCollection(Resource):
    def GET(self, id):
        doc = EnaCollections.find_one({"_id": ObjectId(id)})
        if not doc:
            pass
        return doc

    def PUT(self, doc):
        return EnaCollections.insert(doc)

    def add_ena_study(self, ena_collection_id, study_type_list):
        # first study in list is left blank (flat set to delete though)
        # for the purpose of cloning subsequent ones
        doc = EnaCollections.find_one({"_id": ObjectId(ena_collection_id)})['studies'][0]

        if doc:
            for st in study_type_list:
                study_dict = doc
                study_dict["studyCOPOMetadata"]["id"] = uuid.uuid4().hex
                study_dict["studyCOPOMetadata"]["studyType"] = st['study_type']

                # handles empty study reference assignment
                study_dict["studyCOPOMetadata"]["studyReference"] = ''.join(
                    random.choice(string.ascii_uppercase) for i in range(4))
                if st["study_type_reference"]:
                    study_dict["studyCOPOMetadata"]["studyReference"] = st["study_type_reference"]

                # ...since the model study is deleted by default
                study_dict["studyCOPOMetadata"]["deleted"] = "0"

                EnaCollections.update({"_id": ObjectId(ena_collection_id)},
                                      {"$push": {"studies": study_dict}})

    def clone_ena_study(self, ena_collection_id, cloned_elements):
        doc = EnaCollections.find_one({"_id": ObjectId(ena_collection_id)})['studies'][0]

        if doc:
            study_dict = doc

            study_dict["studyCOPOMetadata"]["id"] = uuid.uuid4().hex
            study_dict["studyCOPOMetadata"]["deleted"] = "0"

            if cloned_elements["studyType"]:
                study_dict["studyCOPOMetadata"]["studyType"] = cloned_elements["studyType"]

            study_dict["studyCOPOMetadata"]["studyReference"] = ''.join(
                random.choice(string.ascii_uppercase) for i in range(4)) + "_CLONE"
            if cloned_elements["studyReference"]:
                study_dict["studyCOPOMetadata"]["studyReference"] = cloned_elements["studyReference"]

            # check for samples and other composite types
            new_samples = []
            for k, v in cloned_elements.items():
                if k[:-2] == "sample":
                    new_samples.append({'id': v, 'deleted': '0'})

            if new_samples:
                study_dict["studyCOPOMetadata"]['samples'] = new_samples

            # get study fields
            ena_d = d_utils.get_ena_ui_template_as_obj().studies.study.fields

            for f in ena_d:
                key_split = f.id.split(".")
                target_key = key_split[len(key_split) - 1]
                if target_key in cloned_elements.keys():
                    study_dict["study"][target_key] = cloned_elements[target_key]

            EnaCollections.update({"_id": ObjectId(ena_collection_id)},
                                  {"$push": {"studies": study_dict}})

    def delete_study(self, ena_collection_id, study_id):
        EnaCollections.update(
            {"_id": ObjectId(ena_collection_id), "studies.studyCOPOMetadata.id": study_id},
            {'$set': {"studies.$.studyCOPOMetadata.deleted": "1"}})

    def add_study_publication(self, study_id, ena_collection_id, auto_fields):
        ena_d = d_utils.get_ena_ui_template_as_obj().studies.study.studyPublications.fields
        auto_fields = ast.literal_eval(auto_fields)

        # get target study
        study = self.get_ena_study(study_id, ena_collection_id)

        # each study should have an empty publication document for creating others
        publication_dict = study["study"]["studyPublications"][0]

        if publication_dict:
            publication_dict["id"] = uuid.uuid4().hex
            publication_dict["deleted"] = "0"

            for f in ena_d:
                key_split = f.id.split(".")
                if f.id in auto_fields.keys():
                    publication_dict[key_split[len(key_split) - 1]] = auto_fields[f.id]

            EnaCollections.update(
                {"_id": ObjectId(ena_collection_id), "studies.studyCOPOMetadata.id": study_id},
                {'$push': {"studies.$.study.studyPublications": publication_dict}})

    def add_study_contact(self, study_id, ena_collection_id, auto_fields):
        ena_d = d_utils.get_ena_ui_template_as_obj().studies.study.studyContacts.fields
        auto_fields = ast.literal_eval(auto_fields)

        # get target study
        study = self.get_ena_study(study_id, ena_collection_id)

        # each study should have an empty contact document for creating others
        contact_dict = study["study"]["studyContacts"][0]

        if contact_dict:
            contact_dict["id"] = uuid.uuid4().hex
            contact_dict["deleted"] = "0"

            for f in ena_d:
                key_split = f.id.split(".")
                if f.id in auto_fields.keys():
                    contact_dict[key_split[len(key_split) - 1]] = auto_fields[f.id]

            EnaCollections.update(
                {"_id": ObjectId(ena_collection_id), "studies.studyCOPOMetadata.id": study_id},
                {'$push': {"studies.$.study.studyContacts": contact_dict}})

    def add_study_protocol(self, study_id, ena_collection_id, auto_fields):
        ena_d = d_utils.get_ena_ui_template_as_obj().studies.study.studyProtocols.fields
        auto_fields = ast.literal_eval(auto_fields)

        # get target study
        study = self.get_ena_study(study_id, ena_collection_id)

        # each study should have an empty protocol document for creating others
        protocol_dict = study["study"]["studyProtocols"][0]

        if protocol_dict:
            protocol_dict["id"] = uuid.uuid4().hex
            protocol_dict["deleted"] = "0"

            for f in ena_d:
                key_split = f.id.split(".")
                if f.id in auto_fields.keys():
                    protocol_dict[key_split[len(key_split) - 1]] = auto_fields[f.id]

            EnaCollections.update(
                {"_id": ObjectId(ena_collection_id), "studies.studyCOPOMetadata.id": study_id},
                {'$push': {"studies.$.study.studyProtocols": protocol_dict}})

    def get_study_publications(self, study_id, ena_collection_id):
        doc = EnaCollections.aggregate([{"$match": {"_id": ObjectId(ena_collection_id)}},
                                        {"$unwind": "$studies"},
                                        {"$match": {"studies.studyCOPOMetadata.id": study_id}},
                                        {"$unwind": "$studies.study.studyPublications"},
                                        {"$match": {"studies.study.studyPublications.deleted": "0"}},
                                        {"$group": {"_id": "$_id",
                                                    "data": {"$push": "$studies.study.studyPublications"}}}])

        return mutil.verify_doc_type(doc)

    def get_study_publication(self, study_id, ena_collection_id, publication_id):
        doc = EnaCollections.aggregate([{"$match": {"_id": ObjectId(ena_collection_id)}},
                                        {"$unwind": "$studies"},
                                        {"$match": {"studies.studyCOPOMetadata.id": study_id}},
                                        {"$unwind": "$studies.study.studyPublications"},
                                        {"$match": {"studies.study.studyPublications.id": publication_id}},
                                        {"$group": {"_id": "$_id",
                                                    "data": {"$push": "$studies.study.studyPublications"}}}])

        data = mutil.verify_doc_type(doc)

        return data[0] if data else {}

    def get_study_publications_all(self, study_id, ena_collection_id):  # this will also include 'deleted' items
        doc = EnaCollections.aggregate([{"$match": {"_id": ObjectId(ena_collection_id)}},
                                        {"$unwind": "$studies"},
                                        {"$match": {"studies.studyCOPOMetadata.id": study_id}},
                                        {"$group": {"_id": "$_id",
                                                    "data": {"$push": "$studies.study.studyPublications"}}}])

        data = mutil.verify_doc_type(doc)

        return data[0] if data else []

    def get_study_contacts(self, study_id, ena_collection_id):
        doc = EnaCollections.aggregate([{"$match": {"_id": ObjectId(ena_collection_id)}},
                                        {"$unwind": "$studies"},
                                        {"$match": {"studies.studyCOPOMetadata.id": study_id}},
                                        {"$unwind": "$studies.study.studyContacts"},
                                        {"$match": {"studies.study.studyContacts.deleted": "0"}},
                                        {"$group": {"_id": "$_id",
                                                    "data": {"$push": "$studies.study.studyContacts"}}}])

        return mutil.verify_doc_type(doc)

    def get_study_contact(self, study_id, ena_collection_id, contact_id):
        doc = EnaCollections.aggregate([{"$match": {"_id": ObjectId(ena_collection_id)}},
                                        {"$unwind": "$studies"},
                                        {"$match": {"studies.studyCOPOMetadata.id": study_id}},
                                        {"$unwind": "$studies.study.studyContacts"},
                                        {"$match": {"studies.study.studyContacts.id": contact_id}},
                                        {"$group": {"_id": "$_id",
                                                    "data": {"$push": "$studies.study.studyContacts"}}}])

        data = mutil.verify_doc_type(doc)

        return data[0] if data else {}

    def get_study_contacts_all(self, study_id, ena_collection_id):  # this will also include 'deleted' items
        doc = EnaCollections.aggregate([{"$match": {"_id": ObjectId(ena_collection_id)}},
                                        {"$unwind": "$studies"},
                                        {"$match": {"studies.studyCOPOMetadata.id": study_id}},
                                        {"$group": {"_id": "$_id",
                                                    "data": {"$push": "$studies.study.studyContacts"}}}])

        data = mutil.verify_doc_type(doc)

        return data[0] if data else []

    def get_study_protocols(self, study_id, ena_collection_id):
        doc = EnaCollections.aggregate([{"$match": {"_id": ObjectId(ena_collection_id)}},
                                        {"$unwind": "$studies"},
                                        {"$match": {"studies.studyCOPOMetadata.id": study_id}},
                                        {"$unwind": "$studies.study.studyProtocols"},
                                        {"$match": {"studies.study.studyProtocols.deleted": "0"}},
                                        {"$group": {"_id": "$_id",
                                                    "data": {"$push": "$studies.study.studyProtocols"}}}])

        return mutil.verify_doc_type(doc)

    def get_study_protocol(self, study_id, ena_collection_id, protocol_id):
        doc = EnaCollections.aggregate([{"$match": {"_id": ObjectId(ena_collection_id)}},
                                        {"$unwind": "$studies"},
                                        {"$match": {"studies.studyCOPOMetadata.id": study_id}},
                                        {"$unwind": "$studies.study.studyProtocols"},
                                        {"$match": {"studies.study.studyProtocols.id": protocol_id}},
                                        {"$group": {"_id": "$_id",
                                                    "data": {"$push": "$studies.study.studyProtocols"}}}])

        data = mutil.verify_doc_type(doc)

        return data[0] if data else {}

    def get_study_protocols_all(self, study_id, ena_collection_id):  # this will also include 'deleted' items
        doc = EnaCollections.aggregate([{"$match": {"_id": ObjectId(ena_collection_id)}},
                                        {"$unwind": "$studies"},
                                        {"$match": {"studies.studyCOPOMetadata.id": study_id}},
                                        {"$group": {"_id": "$_id",
                                                    "data": {"$push": "$studies.study.studyProtocols"}}}])

        data = mutil.verify_doc_type(doc)

        return data[0] if data else []

    def add_ena_sample(self, ena_collection_id, study_type_list, auto_fields):
        ena_d = d_utils.get_ena_ui_template_as_obj().studies.study.studySamples.fields
        auto_fields = ast.literal_eval(auto_fields)

        sample_id = uuid.uuid4().hex
        a = {'id': sample_id}

        characteristics = []

        for f in ena_d:
            key_split = f.id.split(".")
            a[key_split[len(key_split) - 1]] = ""  # accommodates fields not displayed on form
            if f.id in auto_fields.keys():
                a[key_split[len(key_split) - 1]] = auto_fields[f.id]
                if key_split[len(key_split) - 1] == "organism":
                    characteristics.append({
                        "categoryTerm": "organism",
                        "characteristics": auto_fields[f.id],
                        "termSourceREF": auto_fields["termSourceREF_organism"],
                        "termAccessionNumber": auto_fields["termAccessionNumber_organism"]
                    })

        ena_d = d_utils.get_ena_ui_template_as_obj().studies.study.studySamples.sampleCollection.fields

        for f in ena_d:
            key_split = f.id.split(".")
            a[key_split[len(key_split) - 1]] = ""
            if f.id in auto_fields.keys():
                a[key_split[len(key_split) - 1]] = auto_fields[f.id]

        # get characteristics, we have already begun with the organism,
        # retrieve and sort to maintain order as displayed form
        categories = [key for key, value in auto_fields.items() if key.startswith('categoryTerm_')]
        categories.sort()

        for category in categories:
            index_part = category.split("categoryTerm_")[1]
            if auto_fields['categoryTerm_' + index_part]:
                    ch = {
                        "categoryTerm": auto_fields['categoryTerm_' + index_part],
                        "characteristics": auto_fields['characteristics_' + index_part],
                        "termSourceREF": auto_fields['termSourceREF_' + index_part],
                        "termAccessionNumber": auto_fields['termAccessionNumber_' + index_part],
                        "unit": auto_fields['unit_' + index_part]
                    }

                    characteristics.append(ch)

        a["characteristics"] = characteristics

        EnaCollections.update({"_id": ObjectId(ena_collection_id)},
                              {"$push": {"collectionCOPOMetadata.samples": a}})

        # assign sample to studies
        for study_id in study_type_list:
            a = {'id': sample_id, 'deleted': '0'}
            self.add_sample_to_ena_study(study_id, ena_collection_id, a)

        return sample_id

    def edit_ena_sample(self, ena_collection_id, sample_id, study_type_list, auto_fields):
        ena_d = d_utils.get_ena_ui_template_as_obj().studies.study.studySamples.fields
        auto_fields = ast.literal_eval(auto_fields)

        characteristics = []

        for f in ena_d:
            key_split = f.id.split(".")
            if f.id in auto_fields.keys():
                EnaCollections.update(
                    {"_id": ObjectId(ena_collection_id), "collectionCOPOMetadata.samples.id": sample_id},
                    {'$set': {"collectionCOPOMetadata.samples.$." + key_split[len(key_split) - 1]: auto_fields[f.id]}})

                if key_split[len(key_split) - 1] == "organism":
                    characteristics.append({
                        "categoryTerm": "organism",
                        "characteristics": auto_fields[f.id],
                        "termSourceREF": auto_fields["termSourceREF_organism"],
                        "termAccessionNumber": auto_fields["termAccessionNumber_organism"]
                    })

        ena_d = d_utils.get_ena_ui_template_as_obj().studies.study.studySamples.sampleCollection.fields

        for f in ena_d:
            key_split = f.id.split(".")
            if f.id in auto_fields.keys():
                EnaCollections.update(
                    {"_id": ObjectId(ena_collection_id), "collectionCOPOMetadata.samples.id": sample_id},
                    {'$set': {"collectionCOPOMetadata.samples.$." + key_split[len(key_split) - 1]: auto_fields[f.id]}})

        # get characteristics
        #
        categories = [key for key, value in auto_fields.items() if key.startswith('categoryTerm_')]
        categories.sort()

        for category in categories:
            index_part = category.split("categoryTerm_")[1]
            if auto_fields['categoryTerm_' + index_part]:
                    ch = {
                        "categoryTerm": auto_fields['categoryTerm_' + index_part],
                        "characteristics": auto_fields['characteristics_' + index_part],
                        "termSourceREF": auto_fields['termSourceREF_' + index_part],
                        "termAccessionNumber": auto_fields['termAccessionNumber_' + index_part],
                        "unit": auto_fields['unit_' + index_part]
                    }

                    characteristics.append(ch)

        EnaCollections.update(
            {"_id": ObjectId(ena_collection_id), "collectionCOPOMetadata.samples.id": sample_id},
            {'$set': {"collectionCOPOMetadata.samples.$.characteristics": characteristics}})

        # update studies: add sample to study if study in the selected list,
        # delete from study not selected
        studies = EnaCollection().get_ena_studies(ena_collection_id)
        for st in studies:
            study_id = st["studyCOPOMetadata"]["id"]

            a = {'id': sample_id, 'deleted': '1'}
            if study_id in study_type_list:
                a = {'id': sample_id, 'deleted': '0'}

            self.hard_delete_sample_from_study(sample_id, study_id, ena_collection_id)
            self.add_sample_to_ena_study(study_id, ena_collection_id, a)

    def get_ena_sample(self, ena_collection_id, sample_id):
        doc = EnaCollections.find_one({"_id": ObjectId(ena_collection_id),
                                       "collectionCOPOMetadata.samples.id": sample_id},
                                      {"collectionCOPOMetadata.samples.$": 1})

        return doc['collectionCOPOMetadata']['samples'][0] if doc else ''

    # this might have to scale to handle samples at the Profile level
    def get_all_samples(self, ena_collection_id):
        ena_collection = EnaCollection().GET(ena_collection_id)
        samples = ena_collection["collectionCOPOMetadata"]["samples"]

        # the first entry is always a placeholder, and we don't want to include this in the returned data
        del samples[0]

        return samples

    def get_study_samples(self, ena_collection_id, study_id):
        doc = EnaCollections.aggregate([{"$match": {"_id": ObjectId(ena_collection_id)}},
                                        {"$unwind": "$studies"},
                                        {"$match": {"studies.studyCOPOMetadata.id": study_id}},
                                        {"$unwind": "$studies.studyCOPOMetadata.samples"},
                                        {"$match": {"studies.studyCOPOMetadata.samples.deleted": "0"}},
                                        {"$group": {"_id": "$_id",
                                                    "data": {"$push": "$studies.studyCOPOMetadata.samples"}}}])

        return mutil.verify_doc_type(doc)

    def add_sample_to_ena_study(self, study_id, ena_collection_id, sample):
        EnaCollections.update({"_id": ObjectId(ena_collection_id), "studies.studyCOPOMetadata.id": study_id},
                              {'$push': {"studies.$.studyCOPOMetadata.samples": sample}})

    def add_delete_samples_in_study(self, study_id, ena_collection_id, add_list, remove_list):
        if remove_list:
            for sample_id in remove_list:
                self.hard_delete_sample_from_study(sample_id, study_id, ena_collection_id)

        if add_list:
            for sample_id in add_list:
                self.hard_delete_sample_from_study(sample_id, study_id, ena_collection_id)
                a = {'id': sample_id, 'deleted': '0'}
                self.add_sample_to_ena_study(study_id, ena_collection_id, a)

    # this allows the total removal of the specified sample record from a study
    def hard_delete_sample_from_study(self, sample_id, study_id, ena_collection_id):
        EnaCollections.update({"_id": ObjectId(ena_collection_id), "studies.studyCOPOMetadata.id": study_id},
                              {'$pull': {"studies.$.studyCOPOMetadata.samples": {'id': sample_id}}})

    def update_study_publication(self, publication_id, study_id, ena_collection_id, field_list):
        publication = self.get_study_publication(study_id, ena_collection_id, publication_id)
        all_publications = self.get_study_publications_all(study_id, ena_collection_id)

        indx = all_publications.index(publication)

        if indx:
            for f_l in field_list:
                for k, v in f_l.items():
                    EnaCollections.update(
                        {"_id": ObjectId(ena_collection_id), "studies.studyCOPOMetadata.id": study_id},
                        {'$set': {"studies.$.study.studyPublications." + str(indx) + "." + k: v}})

    def update_study_contact(self, contact_id, study_id, ena_collection_id, field_list):
        contact = self.get_study_contact(study_id, ena_collection_id, contact_id)
        all_contacts = self.get_study_contacts_all(study_id, ena_collection_id)

        indx = all_contacts.index(contact)

        if indx:
            for f_l in field_list:
                for k, v in f_l.items():
                    EnaCollections.update(
                        {"_id": ObjectId(ena_collection_id), "studies.studyCOPOMetadata.id": study_id},
                        {'$set': {"studies.$.study.studyContacts." + str(indx) + "." + k: v}})

    def get_ena_study(self, study_id, ena_collection_id):
        doc = EnaCollections.find_one({"_id": ObjectId(ena_collection_id),
                                       "studies.studyCOPOMetadata.id": study_id},
                                      {"studies.studyCOPOMetadata.id.$": 1})

        return doc['studies'][0] if doc else {}

    def get_ena_studies(self, ena_collection_id):
        doc = EnaCollections.aggregate([{"$match": {"_id": ObjectId(ena_collection_id)}}, {"$unwind": "$studies"},
                                        {"$match": {"studies.studyCOPOMetadata.deleted": "0"}},
                                        {"$group": {"_id": "$_id", "data": {"$push": "$studies"}}}])  # using 'data'
        # as a projection variable (in the $group part), allows for harmonising the returned type in verify_doc_type

        return mutil.verify_doc_type(doc)

    def update_study_type(self, ena_collection_id, study_id, elem_dict):
        doc = EnaCollections.update({"_id": ObjectId(ena_collection_id), "studies.studyCOPOMetadata.id": study_id}, {
            '$set': {"studies.$.studyCOPOMetadata.studyType": elem_dict["study_type"],
                     "studies.$.studyCOPOMetadata.studyReference": elem_dict["study_type_reference"]}})
        return doc

    def update_study_details(self, ena_collection_id, study_id, auto_fields):
        ena_d = d_utils.get_ena_ui_template_as_obj().studies.study.fields
        auto_fields = ast.literal_eval(auto_fields)

        auto_dict = {}

        for f in ena_d:
            key_split = f.id.split(".")
            if f.id in auto_fields.keys():
                auto_dict["studies.$.study." + key_split[len(key_split) - 1]] = auto_fields[f.id]

        EnaCollections.update({"_id": ObjectId(ena_collection_id), "studies.studyCOPOMetadata.id": study_id}, {
            '$set': auto_dict})

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
                "_id": ObjectId(ena_study_id)
            },
            spec
        )

    def add_sample_to_study(self, sample, attributes, study_id):
        # create new sample and add to study

        spec_attr = []
        for att_group in attributes:
            tmp = {
                "id": ObjectId(),
                "tag": att_group[0],
                "value": att_group[1],
                "unit": att_group[2],
            }
            spec_attr.append(tmp)
        spec = {
            "_id": ObjectId(),
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
            {"_id": ObjectId(study_id)},
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
        doc = EnaCollections.find_one({"samples._id": ObjectId(sample_id)}, {"samples.$": 1})
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
            {"_id": ObjectId(study_id)},
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

