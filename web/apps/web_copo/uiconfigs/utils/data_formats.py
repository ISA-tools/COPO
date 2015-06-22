from pprint import pprint

__author__ = 'etuka'

import re
import os
import json
import jsonpickle
from collections import namedtuple
import xml.etree.ElementTree as ET
from urllib.request import urlopen
from django.http import HttpResponse

import apps.web_copo.uiconfigs.utils.lookup as lkup
import apps.web_copo.uiconfigs.ena.uimodels.ena_copo_config as ecc
import apps.web_copo.uiconfigs.ena.uimodels.object_model as om
from project_copo.settings.display_messages import SCHEMAS_MESSAGES as SM


# converts from json to dictionary
def json_to_dict(path_to_json):
    template_verify(path_to_json)
    with open(path_to_json, encoding='utf-8') as data_file:
        data = json.loads(data_file.read())

    return data


# converts from json or dictionary to object
def json_to_object(path_or_data):
    if isinstance(path_or_data, dict):
        data = json.loads(json.dumps(path_or_data), object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))
    else:  # assume it is a path to the json file
        template_verify(path_or_data)
        with open(path_or_data, encoding='utf-8') as data_file:
            data = json.loads(data_file.read(), object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))
    return data


def template_verify(path_or_data):
    if not os.path.exists(path_or_data):
        generate_ui_template()


# generates template for UI rendering
def generate_ui_template():
    out_dict = om.OUT_DICT
    out_dict.update({'comment': SM["TEMPLATE_CREATION_WARNING"]})

    new_dict = merge_dicts(do_mapping_ena("INVESTIGATION_FILE"),
                           do_mapping_ena("STUDY_SAMPLE_FILE"),
                           do_mapping_ena("STUDY_ASSAY_GENOME_SEQ_FILE"),
                           do_mapping_ena("STUDY_ASSAY_METAGENOME_SEQ_FILE")
                           )
    out_dict = objectify(new_dict, out_dict)

    # generate and write json to file
    ui_template_json = lkup.SCHEMAS["ENA"]['PATHS_AND_URIS']['UI_TEMPLATE_json']

    json.dump(out_dict, open(ui_template_json, 'w'))

    return out_dict


def refactor_ui_template_ena(request):
    out_dict = generate_ui_template()

    data = {'data': out_dict}
    return HttpResponse(jsonpickle.encode(data))


def do_mapping_ena(arm):
    schema = "ENA"

    tree = ET.parse(urlopen(lkup.SCHEMAS[schema]['PATHS_AND_URIS'][arm]))
    new_dict = ecc.ELEMENTS[arm]
    current_dict = ecc.ELEMENTS[arm]

    root = tree.getroot()

    # get the namespace of the xml document
    ns = namespace(root)

    fields = tree.findall(".//{%s}field" % ns)

    for key, value in current_dict.items():
        attr = lkup.SCHEMAS[schema]['ATTRIBUTE_MAPPINGS']
        # initialise attributes as defined in lookup, maintain default ones defined in the model
        for k in attr:
            if k in value.keys() and current_dict[key][k]:
                new_dict[key].update({k: current_dict[key][k]})
            else:
                new_dict[key].update({k: ''})

        for f in iter(fields):
            # 'ref' key in the config dictionary defined to match 'header' attribute in the xml file
            try:
                if f.get("header") == current_dict[key]["ref"]:
                    for k, v in attr.items():
                        # modify for file field
                        if f.get("is-file-field") == "true" and k == "control":
                            try:
                                # no need retaining the mapping key
                                del new_dict[key][k]
                                new_dict[key].update({k: "file"})
                            except KeyError:
                                pass
                        if not current_dict[key][k]:
                            if v or k == "option_values":
                                if k == "option_values":
                                    # get list values
                                    if f.get("data-type") == "List":
                                        try:
                                            ls = f.findall(".//{%s}list-values" % ns)
                                            options_split = ls[0].text.split(",")
                                            new_dict[key].update({k: options_split})
                                        except IndexError:
                                            pass
                                else:
                                    new_dict[key].update({k: f.get(v)})
                                    if v == "data-type" and f.get(v) in lkup.SCHEMAS[schema]['CONTROL_MAPPINGS'].keys():
                                        new_dict[key].update({k: lkup.SCHEMAS[schema]['CONTROL_MAPPINGS'][f.get(v)]})

            except KeyError:
                pass

    return new_dict


def objectify(source_dict, output_dict):
    new_dict = source_dict
    out_dict = output_dict

    for key in new_dict:
        try:
            # no need retaining the mapping key
            del new_dict[key]["ref"]
            # remove option_values for non select elements
            if not new_dict[key]["control"] == "select":
                del new_dict[key]["option_values"]
        except KeyError:
            pass

        new_dict[key].update({'id': key})
        key_split = key.split(".")

        fmtout = "out_dict"
        if len(key_split) >= 2:
            order = len(key_split) - 1
            for i in range(0, order):
                fmtout += "['" + key_split[i] + "']"
            fmtout += "['fields'].append(new_dict['" + key + "'])"
            eval(fmtout)

    return out_dict


def merge_dicts(*dict_args):
    result = {}
    for dictionary in dict_args:
        result.update(dictionary)
    return result


def namespace(element):
    match = re.search(r'\{(.+)\}', element.tag)
    return match.group(1) if match else ''
