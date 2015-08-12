__author__ = 'etuka'

import json

from collections import namedtuple

from web_copo.copo_maps.utils import lookup
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
    study_types = lookup.DROP_DOWNS['STUDY_TYPES']

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
    path_to_json = lookup.SCHEMAS["ENA"]['PATHS_AND_URIS']['ISA_json']
    data = ""
    with open(path_to_json, encoding='utf-8') as data_file:
        data = json.loads(data_file.read())
    return data

def get_collection_head_dc():
    f_path=lookup.SCHEMAS['COPO']['PATHS_AND_URIS']['COPO_COLLECTION_HEAD_FILE']
    with open(f_path) as json_data:
        data = json.load(json_data)
    return data

