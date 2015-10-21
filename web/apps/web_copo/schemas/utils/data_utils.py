__author__ = 'etuka'

import json
from collections import namedtuple
import re

import web.apps.web_copo.schemas.ena.uimodels.ena_copo_config as ecc
import web.apps.web_copo.schemas.utils.lookup as lkup
from dal import DataSchemas


# converts a dictionary to object
def json_to_object(data_object):
    data = ""
    if isinstance(data_object, dict):
        data = json.loads(json.dumps(data_object), object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))
    return data


def get_label(value, list_of_elements, key_name):
    for dict in list_of_elements:
        return dict["label"] if dict[key_name] == value else ''


def lookup_study_type_label(val):
    # get study types
    study_types = lkup.DROP_DOWNS['STUDY_TYPES']

    for st in study_types:
        if st["value"].lower() == val.lower():
            return st["label"]
    return ""


def get_ena_ui_template_as_dict():
    ui_template = DataSchemas("ENA").get_ui_template()
    return ui_template


def get_ena_ui_template_as_obj():
    ui_template = json_to_object(get_ena_ui_template_as_dict())
    return ui_template


def get_ena_db_template():
    path_to_json = lkup.SCHEMAS["ENA"]['PATHS_AND_URIS']['ISA_json']
    data = ""
    with open(path_to_json, encoding='utf-8') as data_file:
        data = json.loads(data_file.read())
    return data


def get_sample_attributes():
    sample_attributes = json_to_pytype(ecc.MODEL_FILES["SAMPLE_ATTRIBUTES"])
    # maybe some logic here to filter the returned attributes,
    # for instance, based on the tags?
    return sample_attributes


def get_isajson_refactor_type(key):
    out_dict = {}
    if key in json_to_pytype(ecc.MODEL_FILES["ISA_JSON_REFACTOR_TYPES"]):
        out_dict = json_to_pytype(ecc.MODEL_FILES["ISA_JSON_REFACTOR_TYPES"])[key]
    return out_dict


def json_to_pytype(path_to_json):
    data = ""
    with open(path_to_json, encoding='utf-8') as data_file:
        data = json.loads(data_file.read())
    return data


def get_collection_head_dc():
    f_path = lkup.SCHEMAS['COPO']['PATHS_AND_URIS']['COPO_COLLECTION_HEAD_FILE']
    with open(f_path) as json_data:
        data = json.load(json_data)
    return data


